# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import click
import translations


@click.command()
def main():
    translations.run()
    click.echo(click.style('Done', fg='green'))

if __name__ == '__main__':
    main()
