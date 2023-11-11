import click


@click.command()
@click.option(
    "-s",
    "--src",
    prompt="Source folder",
    help="Source folder from where files are picked up.",
)
@click.option(
    "-d",
    "--dst",
    prompt="Destination folder",
    help="Destination folder where files will be copied.",
)
@click.option(
    "-u",
    "--used",
    help=(
        "Folder where picked up files will be moved. "
        "When not specified it's assumed '{Source Folder}/seen'."
    ),
)
@click.option(
    "-n",
    "--num-files",
    type=click.INT,
    prompt="Num files",
    help="Number of files to be picked up.",
)
@click.option(
    "--glob",
    default=["*"],
    show_default=True,
    multiple=True,
    help=(
        "Pattern for selecting files in source folder. "
        "Can be used multiple times."
    ),
)
def cli(src, dst, used, num_files, glob):
    """Randomly picks Num-Files files from a Source Folder according to the
    given glob patterns, copying them to a Destination Folder, and moving
    selected files to the used folder so that they're not eligible for
    subsequent picking.
    """
    if not used:
        used = f"{dst}/seen"
    click.echo(
        f"src={src}, dst={dst}, used={used}, num_files={num_files}, glob={glob}"
    )
