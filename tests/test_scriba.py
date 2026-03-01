import io

from scriba import format_timestamp, write_srt, write_txt, write_vtt

SEGMENTS = [
    {"start": 0.0, "end": 2.5, "text": " Hello world"},
    {"start": 2.5, "end": 5.0, "text": " How are you"},
]


class TestFormatTimestamp:
    def test_vtt_format(self):
        assert format_timestamp(0.0, "vtt") == "00:00:00.000"
        assert format_timestamp(61.5, "vtt") == "00:01:01.500"
        assert format_timestamp(3661.123, "vtt") == "01:01:01.123"

    def test_srt_format_uses_comma(self):
        assert format_timestamp(0.0, "srt") == "00:00:00,000"
        assert format_timestamp(61.5, "srt") == "00:01:01,500"

    def test_large_timestamp(self):
        assert format_timestamp(86399.999, "vtt") == "23:59:59.999"


class TestWriteTxt:
    def test_joins_segments(self):
        buf = io.StringIO()
        write_txt(SEGMENTS, buf)
        assert buf.getvalue() == "Hello world How are you"

    def test_empty_segments(self):
        buf = io.StringIO()
        write_txt([], buf)
        assert buf.getvalue() == ""


class TestWriteSrt:
    def test_format(self):
        buf = io.StringIO()
        write_srt(SEGMENTS, buf)
        lines = buf.getvalue()
        assert lines.startswith("1\n00:00:00,000 --> 00:00:02,500\nHello world\n")
        assert "2\n00:00:02,500 --> 00:00:05,000\nHow are you\n" in lines

    def test_numbering_starts_at_one(self):
        buf = io.StringIO()
        write_srt(SEGMENTS, buf)
        first_line = buf.getvalue().split("\n")[0]
        assert first_line == "1"


class TestWriteVtt:
    def test_starts_with_header(self):
        buf = io.StringIO()
        write_vtt(SEGMENTS, buf)
        assert buf.getvalue().startswith("WEBVTT\n\n")

    def test_no_numbering(self):
        buf = io.StringIO()
        write_vtt(SEGMENTS, buf)
        lines = buf.getvalue().split("\n")
        # After "WEBVTT" and blank line, next line is a timestamp, not a number
        assert "-->" in lines[2]
