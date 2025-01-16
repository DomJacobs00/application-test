import pytest
import tempfile
from main import main

@pytest.fixture
def sample_input_file():
    data = """2025-01-01T01:00:00Z, 10
2025-01-01T02:00:00Z, 15
2025-01-01T03:00:00Z, 15
2025-01-01T04:00:00Z, 13"""
    tempFile = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
    tempFile.write(data)
    tempFile.close()
    return tempFile.name

@pytest.fixture
def temp_output_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
    temp_file.close()
    return temp_file.name


def test_main(sample_input_file, temp_output_file, monkeypatch):
    original_open = open

    def mock_open(path, *args, **kwargs):
        if path == 'input.csv':
            return original_open(sample_input_file, *args, **kwargs)
        if path == 'output.csv':
            return original_open(temp_output_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)
        
    monkeypatch.setattr('builtins.open', mock_open)

    output_data = []

    def mock_csv_writer(file):
        class MockWriter:
            def writerow(self, row):
                output_data.append(row)
            def writerows(self, rows):
                output_data.extend(rows)
        return MockWriter()
    
    monkeypatch.setattr('csv.writer', mock_csv_writer)


    main()


    expected_output = [
        ['2025-01-01T01:00:00Z', 10],
        ['2025-01-01T01:58:00Z', 10],
        ['2025-01-01T02:02:00Z', 15],
        ['2025-01-01T03:59:00Z', 15],
        ['2025-01-01T04:01:00Z', 13],
    ]

    assert output_data == expected_output