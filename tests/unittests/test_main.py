from src.main import main


def test_main():

    result = main()

    assert result == "Hello from python-template!"
