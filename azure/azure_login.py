# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Nathan Embery nembery@paloaltonetworks.com

import io
import json
import sys

from azure.cli.core import get_default_cli

output = io.StringIO()

sys.sterr = sys.stdout

is_logged_in_output = io.StringIO()
get_default_cli().invoke(['account', "show"], out_file=is_logged_in_output)

if 'environmentName' not in is_logged_in_output.getvalue():
    get_default_cli().invoke(['login', "--use-device-code"], out_file=sys.stdout)

# capture return code for issue #1
r = get_default_cli().invoke(['account', "list"], out_file=output)

accounts_str = output.getvalue()
try:
    accounts_json = json.loads(accounts_str)

    account_list = list()
    for account in accounts_json:
        out_dict = dict()
        out_dict['key'] = account.get('name', 'Unknown Name')
        out_dict['value'] = account.get('id', 'Unknown Id')
        account_list.append(out_dict)

    account_lst_encoded = json.dumps(account_list)
    print(f'###{account_lst_encoded}###')

except ValueError:
    print('Could not get list of accounts in Azure')
    sys.exit(1)

sys.exit(r)
