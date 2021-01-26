import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

@click.group()
def cli():
    pass

def inner_text():
    innertext = ""
    with open('templates/create_inner.html', 'r') as innerfile:
        innertext = innerfile.read()
        return innertext

@click.command()
def generate():
    with open('templates/create_outer.html','r') as outerfile:
        innertext = inner_text()
        outertext = outerfile.read()
        outertext = outertext.replace('___replace_content___', innertext)
        print(outertext)
    

@click.command()
def list():
    click.echo('Dropped the database')

cli.add_command(generate)
cli.add_command(list)
if __name__ == '__main__':
    cli()