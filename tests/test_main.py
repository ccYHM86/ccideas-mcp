from ccideas_mcp.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from ccideas-mcp!" in captured.out
