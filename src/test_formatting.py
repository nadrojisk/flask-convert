from formatting import *


def test_hex_to_hex():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = hex_to_hex(text)
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_hex_to_hex_multi_byte():
    text = "0x3031"
    actual = hex_to_hex(text)
    expected = "0x3031"

    assert expected == actual


def test_bin_to_hex():
    text = "0b00110000 0b00110001 0b00110010 0b00110011 0b00110100 0b00110101 0b01000001 0b01000010"
    actual = bin_to_hex(text).strip()
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_bin_to_hex_multi_byte():
    text = "0b11000000110001"
    actual = bin_to_hex(text).strip()
    expected = "0x3031"

    assert expected == actual


def test_dec_to_hex():
    text = "48 49 50 51 52 53 65 66"
    actual = dec_to_hex(text).strip()
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_dec_to_hex_multi_byte():
    text = "12337"
    actual = dec_to_hex(text).strip()
    expected = "0x3031"

    assert expected == actual


def test_oct_to_hex():
    text = "0o060 0o061 0o062 0o063 0o064 0o065 0o101 0o102"
    actual = oct_to_hex(text).strip()
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_oct_to_hex_multi_byte():
    text = "0o30061"
    actual = oct_to_hex(text).strip()
    expected = "0x3031"

    assert expected == actual


def test_base64_to_hex():
    text = "MDEyMzQ1QUI="
    actual = base64_to_hex(text).strip()
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_base32_conversion_normal():
    text = "GAYTEMZUGVAUE==="
    actual = base32_to_hex(text).strip()
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual
