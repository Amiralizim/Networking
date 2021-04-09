import CLI.commands
import unittest
import mock
from click.testing import CliRunner
from unittest.mock import patch

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TestClientRoute(unittest.TestCase):
    
    @mock.patch('commands.client_option')
    @mock.patch('click.secho')
    def test_login(self, click_secho_mocked, client_option_mocked):
        runner = CliRunner()
        runner.invoke(
            commands.login, '--username admin --password password123'.split(), input='2'
        )
        click_secho_mocked.assert_called_with("Succesfully logged in!", fg = 'green')
        print(bcolors.OKGREEN  + "Login test passed" + u' \u2713' + bcolors.ENDC)

    @mock.patch('click.secho')
    def test_client_options(self, click_secho_mocked):
        runner = CliRunner()
        runner.invoke(
            commands.client_option, '--clientchoice privateIps'.split(), input='1'
        )
        click_secho_mocked.assert_called_with("example:  10.200.7.194", fg="yellow")
        print(bcolors.OKGREEN  + "Client option test passed" + u' \u2713' + bcolors.ENDC)
          
    @mock.patch('commands.src_port_selection')
    @mock.patch('commands.mode', "private")
    def test_src_ip_selection(self, src_port_selection_mocked):
        runner = CliRunner()
        runner.invoke(
            commands.src_ip_selection, '--source_ip 10.200.7.194'.split(), input='1'
        )
        src_port_selection_mocked.assert_called_with(None)
        print(bcolors.OKGREEN  + "Src ip test passed" + u' \u2713' +  bcolors.ENDC)

    @mock.patch('click.secho')
    @mock.patch('commands.mode', "private")
    def test_src_port_selection_failure(self, click_secho_mocked):
        '''test the failure case'''
        runner = CliRunner()
        runner.invoke(
            commands.src_port_selection, '--sourceport invalid'.split(), input='1'
        )
        click_secho_mocked.assert_called_with("incorrect value, try again!", fg="red")
        print(bcolors.OKGREEN  + "Src port failute test passed" + u' \u2713' + bcolors.ENDC)

    @mock.patch('commands.dst_ip_selection')
    @mock.patch('commands.mode', "private")
    def test_src_port_selection(self, dst_ip_selection_mocked):
        runner = CliRunner()
        runner.invoke(
            commands.src_port_selection, '--sourceport 32827'.split(), input='1'
        )
        dst_ip_selection_mocked.assert_called_with(None)
        print(bcolors.OKGREEN  + "Src port test passed" + u' \u2713' + bcolors.ENDC)

    @mock.patch('commands.dst_port_selection')
    @mock.patch('commands.mode', "private")
    @mock.patch('commands.src_ip', "10.200.7.194")
    @mock.patch('commands.src_port', "32827")
    def test_dst_ip_selection(self, dst_port_selection_mocked):
        runner = CliRunner()
        runner.invoke(
            commands.dst_ip_selection, '--dstip 179.1.4.230'.split(), input='1'
        )
        dst_port_selection_mocked.assert_called_with(None)
        print(bcolors.OKGREEN  + "Dst ip test passed" + u' \u2713' + bcolors.ENDC)

    @mock.patch('commands.generate_flow_index')
    @mock.patch('commands.mode', "private")
    @mock.patch('commands.src_ip', "10.200.7.194")
    @mock.patch('commands.src_port', "32827")
    @mock.patch('commands.dst_ip', "179.1.4.230")
    def test_dst_port_selection(self, generate_flow_index_mocked):
        src_ip = "10.200.7.194"
        src_port = "32827"
        dst_ip = "179.1.4.230"
        dst_port = "443"
        runner = CliRunner()
        runner.invoke(
            commands.dst_port_selection, '--dstport 443'.split(), input='1'
        )
        generate_flow_index_mocked.assert_called_with(src_ip, dst_ip, src_port, dst_port)
        print(bcolors.OKGREEN  + "Dst port test passed" + u' \u2713' + bcolors.ENDC)

    @mock.patch('commands.find_flows')
    @mock.patch('commands.display_or_annotate')
    def test_generate_flow_index(self, display_or_annotate_mocked, find_flows_mocked):
        src_ip = "10.200.7.194"
        src_port = "32827"
        dst_ip = "179.1.4.230"
        dst_port = "443"
        link_id = src_ip+'-'+src_port+'-'+dst_ip+'-'+dst_port
        commands.generate_flow_index(src_ip, dst_ip, src_port, dst_port)
        find_flows_mocked.assert_called_with(link_id)
        print(bcolors.OKGREEN  + "Flow index test passed" + u' \u2713' + bcolors.ENDC)


    


        