"""Testing setup_logger function"""
import unittest
from collections import namedtuple


from randfpck import setup_arg_parser


class TestArgParserSetup(unittest.TestCase):
    """Test the setup_argparser function"""

    def test_description_not_empty(self):
        """Validates that the parser has some description"""
        parser = setup_arg_parser()
        self.assertIsNotNone(
            parser.description, "expected parser.description to be not None, but was None"
        )
        self.assertNotEqual(
            parser.description, "", "expected parser.description not to be empty, but was ''"
        )

    def test_parser_unhappy_path(self):
        """Unhappy path for arg parsing"""
        parser = setup_arg_parser()

        TestCase = namedtuple("TestCase", ["cli_args"])
        test_cases = {
            "No args": TestCase(cli_args=None),
            "Empty string args": TestCase(cli_args=""),
            "Empty array args": TestCase(cli_args=[]),
            "Only source": TestCase(cli_args=["-s", "src_folder/"]),
            "Only dst": TestCase(cli_args=["-d", "dst_folder/"]),
            "Only glob": TestCase(cli_args=["-g", "glob.*"]),
            "Only num files": TestCase(cli_args=["-n", "5"]),
            "Only used (optional)": TestCase(cli_args=["-u", "used_folder/"]),
            "Source and dst": TestCase(cli_args=["-s", "src_folder/", "-d", "dst_folder/"]),
            "Source and glob": TestCase(cli_args=["-s", "src_folder/", "-g", "glob.*"]),
            "Source and num files": TestCase(cli_args=["-s", "src_folder/", "-n", "5"]),
            "Source, dst, and glob": TestCase(
                cli_args=["-s", "src_folder/", "-d", "dst_folder/", "-g", "glob.*"]
            ),
            "Source, dst, and num files": TestCase(
                cli_args=["-s", "src_folder/", "-d", "dst_folder/", "-n", "5"]
            ),
            "Source, dst, num files and used": TestCase(
                cli_args=["-s", "src_folder/", "-d", "dst_folder/", "-n", "5", "-u", "used/"]
            ),
            "num must be a number": TestCase(
                cli_args=["-n", "a", "-s", "src_folder/", "-d", "dst_folder/", "-g", "glob.*"]
            ),
        }

        for test_case, test_data in test_cases.items():
            cli_args = test_data.cli_args
            with self.assertRaises(
                SystemExit, msg=f"{test_case}: expected exception but nothing was raised"
            ) as ex:
                parser.parse_args(cli_args)

            self.assertEqual(ex.exception.code, 2)

    def test_parser_happy_path_req_args(self):
        """Happy path for arg parsing when providing only required args"""
        parser = setup_arg_parser()

        try:
            args = parser.parse_args(
                ["-s", "src_folder/", "-d", "dst_folder/", "-g", "glob.*", "-n", "5"]
            )
        except (Exception, SystemExit) as e:  # pylint: disable=broad-exception-caught,invalid-name
            self.fail(f"exception not expected, but got {type(e)}")
        else:
            self.assertEqual(
                args.src, "src_folder/", f"expected 'src_folder/' but got {args.src!r}"
            )
            self.assertEqual(
                args.dst, "dst_folder/", f"expected 'dst_folder/' but got {args.dst!r}"
            )
            self.assertListEqual(args.glob, ["glob.*"], f"expected ['glob.*'] but got {args.glob}")
            self.assertEqual(args.num_files, 5, f"expected 5 but got {args.num_files}")

    def test_parser_happy_path_with_opt_args(self):
        """Happy path for arg parsing when providing required and optional args"""
        parser = setup_arg_parser()

        try:
            args = parser.parse_args(
                [
                    "-s",
                    "src_folder/",
                    "-d",
                    "dst_folder/",
                    "-g",
                    "glob.*",
                    "-n",
                    "5",
                    "-u",
                    "used_folder/",
                ]
            )
        except (Exception, SystemExit) as e:  # pylint: disable=broad-exception-caught,invalid-name
            self.fail(f"exception not expected, but got {type(e)}")
        else:
            self.assertEqual(
                args.src, "src_folder/", f"expected 'src_folder/' but got {args.src!r}"
            )
            self.assertEqual(
                args.dst, "dst_folder/", f"expected 'dst_folder/' but got {args.dst!r}"
            )
            self.assertEqual(
                args.used, "used_folder/", f"expected 'used_folder/' but got {args.used!r}"
            )
            self.assertListEqual(args.glob, ["glob.*"], f"expected ['glob.*'] but got {args.glob}")
            self.assertEqual(args.num_files, 5, f"expected 5 but got {args.num_files}")

    def test_parser_happy_path_with_multipl_glob(self):
        """Happy path for arg parsing when providing multiple glob patterns"""
        parser = setup_arg_parser()

        try:
            args = parser.parse_args(
                [
                    "-s",
                    "src_folder/",
                    "-d",
                    "dst_folder/",
                    "-g",
                    "glob1.*",
                    "glob2",
                    "*glob3*.txt",
                    "-n",
                    "5",
                ]
            )
        except (Exception, SystemExit) as e:  # pylint: disable=broad-exception-caught,invalid-name
            self.fail(f"exception not expected, but got {type(e)}")
        else:
            self.assertEqual(
                args.src, "src_folder/", f"expected 'src_folder/' but got {args.src!r}"
            )
            self.assertEqual(
                args.dst, "dst_folder/", f"expected 'dst_folder/' but got {args.dst!r}"
            )
            self.assertListEqual(
                args.glob,
                ["glob1.*", "glob2", "*glob3*.txt"],
                f'expected ["glob1.*", "glob2", "*glob3*.txt"] but got {args.glob}',
            )
            self.assertEqual(args.num_files, 5, f"expected 5 but got {args.num_files}")


if __name__ == "__main__":
    unittest.main(buffer=True)  # buffer=True removes info on stdout
