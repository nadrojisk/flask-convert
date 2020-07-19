from utilities import *


def test_ascii_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = ascii_conversion(text)
    expected = "012345AB"

    assert expected == actual


def test_ascii_conversion_unicode():
    text = "0x3010"
    actual = ascii_conversion(text)
    expected = '【'

    assert expected == actual


def test_bin_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = bin_conversion(text)
    expected = "0b00110000 0b00110001 0b00110010 0b00110011 0b00110100 0b00110101 0b01000001 0b01000010"

    assert expected == actual


def test_bin_conversion_muti_byte():
    text = "0x3031"
    actual = bin_conversion(text)
    expected = "0b11000000110001"

    assert expected == actual


def test_dec_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = dec_conversion(text)
    expected = "48 49 50 51 52 53 65 66"

    assert expected == actual


def test_dec_conversion_multi_byte():
    text = "0x3031"
    actual = dec_conversion(text)
    expected = "12337"

    assert expected == actual


def test_hex_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = hex_conversion(text)
    expected = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"

    assert expected == actual


def test_hex_conversion_multi_byte():
    text = "0x3031"
    actual = hex_conversion(text)
    expected = "0x3031"

    assert expected == actual


def test_oct_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = oct_conversion(text)
    expected = "0o060 0o061 0o062 0o063 0o064 0o065 0o101 0o102"

    assert expected == actual


def test_oct_conversion_multi_byte():
    text = "0x3031"
    actual = oct_conversion(text)
    expected = "0o30061"

    assert expected == actual


def test_base64_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = base64_conversion(text)
    expected = "MDEyMzQ1QUI="

    assert expected == actual


def test_base32_conversion_normal():
    text = "0x30 0x31 0x32 0x33 0x34 0x35 0x41 0x42"
    actual = base32_conversion(text)
    expected = "GAYTEMZUGVAUE==="

    assert expected == actual
