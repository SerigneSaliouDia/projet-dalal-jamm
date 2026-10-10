"""Tests de read_header sur des DICOM SYNTHÉTIQUES (aucune donnée réelle)."""

from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import UID, ExplicitVRLittleEndian, generate_uid

from dalal_jamm.dicom.inventory import build_inventory
from dalal_jamm.dicom.metadata import COLUMNS, read_header

MG_PRESENTATION = UID("1.2.840.10008.5.1.4.1.1.1.2")


def make_dicom(path, with_preamble=True, **fields):
    """Écrit un petit DICOM fictif (sans pixels)."""
    ds = Dataset()
    ds.SOPClassUID = MG_PRESENTATION
    ds.SOPInstanceUID = generate_uid()
    ds.Modality = "MG"
    for key, value in fields.items():
        setattr(ds, key, value)
    if with_preamble:
        meta = FileMetaDataset()
        meta.MediaStorageSOPClassUID = ds.SOPClassUID
        meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
        meta.TransferSyntaxUID = ExplicitVRLittleEndian
        ds.file_meta = meta
        try:
            ds.save_as(path, enforce_file_format=True)
        except TypeError:  # pydicom 2.x
            ds.is_little_endian, ds.is_implicit_VR = True, False
            ds.save_as(path, write_like_original=False)
    else:
        try:
            ds.save_as(path, implicit_vr=True, little_endian=True)
        except TypeError:  # pydicom 2.x
            ds.is_little_endian, ds.is_implicit_VR = True, True
            ds.save_as(path, write_like_original=True)
    return path


def test_valid_file_is_read(tmp_path):
    f = make_dicom(
        tmp_path / "a.IMA",
        PatientName="TEST^FICTIF", PatientID="ID123", StudyDate="20260413",
        ImageLaterality="R", ViewPosition="CC", SeriesDescription="MAMMOGRAM, Diagnosis",
        PresentationIntentType="FOR PRESENTATION", Rows=3328, Columns=2560,
    )
    r = read_header(f)
    assert r["status"] == "ok" and r["error"] is None
    assert r["image_laterality"] == "R" and r["view_position"] == "CC"
    assert r["series_description"] == "MAMMOGRAM, Diagnosis"
    assert r["presentation_intent"] == "FOR PRESENTATION"
    assert (r["rows"], r["columns"]) == ("3328", "2560")
    assert r["study_date"] == "20260413"
    assert r["transfer_syntax"] == str(ExplicitVRLittleEndian)
    assert r["ident_patient_name"] == "TEST^FICTIF"


def test_missing_fields_stay_empty_not_invented(tmp_path):
    r = read_header(make_dicom(tmp_path / "b.IMA"))
    assert r["status"] == "ok"
    assert r["image_laterality"] is None and r["view_position"] is None
    assert r["series_description"] is None and r["rows"] is None


def test_empty_string_is_treated_as_absent(tmp_path):
    r = read_header(make_dicom(tmp_path / "c.IMA", ImageLaterality="", ViewPosition="  "))
    assert r["image_laterality"] is None and r["view_position"] is None


def test_file_without_preamble_is_read_but_flagged(tmp_path):
    r = read_header(make_dicom(tmp_path / "d.IMA", with_preamble=False, ImageLaterality="L", ViewPosition="MLO"))
    assert r["status"] == "forced"
    assert (r["image_laterality"], r["view_position"]) == ("L", "MLO")


def test_non_dicom_file_is_error(tmp_path):
    f = tmp_path / "e.IMA"
    f.write_text("ceci n'est pas un DICOM " * 20)
    r = read_header(f)
    assert r["status"] == "error" and r["error"]


def test_missing_file_does_not_raise(tmp_path):
    r = read_header(tmp_path / "n_existe_pas.IMA")
    assert r["status"] == "error" and r["error"] == "FileNotFoundError"


def test_errors_never_leak_the_path(tmp_path):
    secret = "NOM_SECRET_PATIENTE"
    f = tmp_path / f"{secret}.IMA"
    f.write_text("pas du dicom " * 20)
    assert secret not in repr(read_header(f))
    assert secret not in repr(read_header(tmp_path / f"{secret}_absent.IMA"))


def test_result_always_has_all_columns(tmp_path):
    for r in (read_header(make_dicom(tmp_path / "f.IMA")), read_header(tmp_path / "zzz.IMA")):
        assert list(r.keys()) == COLUMNS


def test_build_inventory_joins_files_and_headers(tmp_path):
    ser = tmp_path / "PAT_A" / "EX1" / "SERIE_2"
    ser.mkdir(parents=True)
    make_dicom(ser / "x1.IMA", ImageLaterality="R", ViewPosition="CC")
    make_dicom(ser / "x2.IMA", ImageLaterality="L", ViewPosition="CC")
    (ser / "x3.IMA").write_text("pas du dicom " * 20)
    df = build_inventory(tmp_path)
    assert len(df) == 3
    assert df["status"].value_counts().to_dict() == {"ok": 2, "error": 1}
    row = df.set_index("rel_path").loc["PAT_A/EX1/SERIE_2/x2.IMA"]
    assert (row["image_laterality"], row["view_position"], row["series_folder"]) == ("L", "CC", "SERIE_2")
