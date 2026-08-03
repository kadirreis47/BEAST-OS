from beastos.cli.app import build_parser

def test_parser():
 assert build_parser().parse_args(['dashboard']).command=='dashboard'
