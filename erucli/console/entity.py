# coding: utf-8
import os

import click
from eruhttp import EruException

from erucli.console.output import as_form
from erucli.console.style import error, info


@click.argument('name')
@click.argument('description', default='')
@click.pass_context
def create_pod(ctx, name, description):
    eru = ctx.obj['eru']
    try:
        eru.create_pod(name, description)
        click.echo(info('Pod created successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('name')
@click.argument('cidr')
@click.pass_context
def create_network(ctx, name, cidr):
    eru = ctx.obj['eru']
    try:
        eru.create_network(name, cidr)
        click.echo(info('Network created successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('addr')
@click.argument('pod_name')
@click.option('--public/--private', default=False)
@click.option('--docker-cert-path', default='')
@click.pass_context
def create_host(ctx, addr, pod_name, public, docker_cert_path=''):
    eru = ctx.obj['eru']
    try:
        if docker_cert_path:
            domain = addr.split(':')[0]
            this_host_cert_path = os.path.join(docker_cert_path, domain)

        eru.create_host(addr, pod_name, docker_cert_path=this_host_cert_path, is_public=public)
        click.echo(info('Host {} assigned to {} successfully'.format(addr, pod_name)))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('hostname')
@click.pass_context
def host_bind_eip(ctx, hostname):
    eru = ctx.obj['eru']
    try:
        r = eru.bind_host_eip(hostname)
        click.echo(info('EIP %s bind successfully' % r['eip']))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('hostname')
@click.pass_context
def host_release_eip(ctx, hostname):
    eru = ctx.obj['eru']
    try:
        eru.release_host_eip(hostname)
        click.echo(info('EIP release successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('hostname')
@click.pass_context
def host_get_eip(ctx, hostname):
    eru = ctx.obj['eru']
    try:
        r = eru.get_host_eip(hostname)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['EIP', 'used']
        content = [[eip, '*' if u else ''] for (eip, u) in r.iteritems()]
        as_form(title, content)
