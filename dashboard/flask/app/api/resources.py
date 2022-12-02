from flask_restful import Resource, reqparse
import asyncio
import os


async def command(cmd):
    """
    Execute a command on the system asynchronously
    """
    await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)


class StartHping(Resource):
    @staticmethod
    def post(partner: str):
        print('POST StartHping')
        if partner not in [p.lower().replace(' ', '-') for p in os.getenv('PARTNERS').split(':')]:
            return {'Error': f'partner {partner} is not in the list of partners in this pilot.'}, 400

        target = os.getenv(f'{partner.upper()}_TARGET')
        protocol_options = {'tcp': '', 'udp': '--udp', 'icmp': '--icmp', 'rawip': '--rawip'}
        speed_options = ['u1000000', 'u100000', 'u10000', 'u1000', 'u100', 'u10', 'u1', 'u0']

        # Parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('protocol', choices=list(protocol_options.keys()), required=True, location='form')
        parser.add_argument('duration', type=int, required=True, location='form')
        parser.add_argument('speed', choices=speed_options, required=True, location='form')
        parser.add_argument('port', type=int, location='form')
        parser.add_argument('data', type=int, location='form')
        parser.add_argument('icmp_type', type=int, location='form')
        parser.add_argument('icmp_code', type=int, location='form')
        parser.add_argument('ip_proto', type=int, location='form')
        parser.add_argument('syn', location='form')
        parser.add_argument('ack', location='form')
        parser.add_argument('fin', location='form')
        parser.add_argument('fragment', location='form')
        parser.add_argument('no_frag', location='form')
        parser.add_argument('more_frag', location='form')
        args = parser.parse_args()
        print(args)

        # Validate arguments and construct hping3 command flags
        flags = ['--quiet']

        if type(args.duration) != int or args.duration > 120 or args.duration < 1:
            return {'Error': 'Duration must be a positive integer under 120.'}, 400

        if args.protocol not in protocol_options:
            return {'Error': 'Invalid protocol argument.'}, 400
        flags.append(protocol_options[args.protocol])

        if args.speed not in speed_options:
            return {'Error': 'Invalid packet speed argument.'}, 400
        flags.append(f"-i {args.speed}")

        if args.port is not None:
            if type(args.port) != int or args.port < 1 or args.port > 65535:
                return {'Error': 'Port number should be between 1 and 65535.'}, 400
            flags.append(f"-p {args.port}")

        if args.data is not None:
            if type(args.data) != int or args.data < 0 or args.data > 1000:
                return {'Error': 'Nr of data bytes per packet should be between 1 and 1000.'}, 400
            flags.append(f"-d {args.data}")

        if args.icmp_type is not None:
            if type(args.icmp_type) != int or args.icmp_type < 0 or args.icmp_type > 18:
                return {'Error': 'ICMP type should be between 1 and 18.'}, 400
            flags.append(f"--icmptype {args.icmp_type}")

        if args.icmp_code is not None:
            if type(args.icmp_code) != int or args.icmp_code < 0 or args.icmp_code > 15:
                return {'Error': 'ICMP code should be between 1 and 15.'}, 400
            flags.append(f"--icmpcode {args.icmp_code}")

        if args.ip_proto is not None:
            if type(args.ip_proto) != int or args.ip_proto < 0 or args.ip_proto > 143:
                return {'Error': 'IP Protocol number should be between 1 and 143.'}, 400
            flags.append(f"--ipproto {args.ip_proto}")

        if args.fragment is not None:
            flags.append('--frag')

        if args.no_frag is not None:
            flags.append('--dontfrag')

        if args.more_frag is not None:
            flags.append('--morefrag')

        if args.syn is not None:
            flags.append('--syn')

        if args.ack is not None:
            flags.append('--ack')

        if args.fin is not None:
            flags.append('--fin')

        flags = ' '.join(flags)
        print(flags)

        try:
            if partner == 'demo':
                prime_target = f"""ansible-playbook -i /ansible/inventory /ansible/prime_target.yml --extra-vars "duration={args.duration + 5}" """
                print("Priming target")
                asyncio.run(command(prime_target))

            instructions = f"""ansible-playbook -i /ansible/inventory /ansible/attacks/hping.yml --extra-vars "duration={args.duration} target={target} flags='{flags}'" """
            print(f"Running: {instructions}")
            asyncio.run(command(instructions))
        except KeyError:
            return {'Error': 'Invalid attack type.'}, 400

        return {'message': f'Started hping3 with flags {flags}!'}, 200


class StartPlaybook(Resource):
    @staticmethod
    def start_command(partner: str, playbook: str, protocol: str = ''):
        if partner not in [p.lower().replace(' ', '-') for p in os.getenv('PARTNERS').split(':')]:
            return {'Error': f'partner {partner} is not in the list of partners in this pilot.'}, 400

        target = os.getenv(f'{partner.upper()}_TARGET')
        # Parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('duration', type=int, required=True)
        args = parser.parse_args()
        print(args)

        if type(args.duration) != int or args.duration > 120 or args.duration < 1:
            return {'Error': 'Duration must be a positive integer under 120.'}, 400

        try:
            if partner == 'demo':
                prime_target = f"""ansible-playbook -i /ansible/inventory /ansible/prime_target.yml --extra-vars "duration={args.duration + 5}" """
                print("Priming target")
                asyncio.run(command(prime_target))

            instructions = f'ansible-playbook -i /ansible/inventory /ansible/attacks/{playbook} --extra-vars ' \
                           f'"duration={args.duration} target={protocol}{target}" '
            print(f"Running: {instructions}")
            asyncio.run(command(instructions))
        except KeyError:
            return {'Error': 'Invalid attack type.'}, 400

        return {'message': f'Started GoldenEye'}, 200


class StartGoldenEye(StartPlaybook):
    @staticmethod
    def post(partner: str):
        StartPlaybook.start_command(partner=partner, playbook='goldeneye.yml', protocol='http://')


class StartHULK(StartPlaybook):
    @staticmethod
    def post(partner: str):
        StartPlaybook.start_command(partner=partner, playbook='hulk.yml', protocol='http://')


class StartLOIC(StartPlaybook):
    @staticmethod
    def post(partner: str):
        StartPlaybook.start_command(partner=partner, playbook='loic.yml')


class StartSlowloris(StartPlaybook):
    @staticmethod
    def post(partner: str):
        StartPlaybook.start_command(partner=partner, playbook='slowloris.yml')


class Stop(Resource):
    @staticmethod
    def post(partner: str):
        if partner not in [p.lower().replace(' ', '-') for p in os.getenv('PARTNERS').split(':')]:
            return {'error': f'partner {partner} is not in the list of partners in this pilot.'}, 400

        target = os.getenv(f'{partner.upper()}_TARGET')
        target = f'[{target[0]}]{target[1:]}'  # [t]arget (for better grep)

        instructions = f'ansible-playbook -i /ansible/inventory /ansible/attacks/stop.yml --extra-vars ' \
                       f'"target={target}" '
        print(f"Running: {instructions}")
        asyncio.run(command(instructions))
        return {'message': f'Stopped!'}, 200
