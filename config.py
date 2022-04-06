# Config file for PGP Encrypter / Version: GnuPG v2.0.22 (GNU/Linux)
gpg_recipients = 'uac-agent.dev.svc@amherst.com'
homedir = "/home/uac-agent.dev.svc@corp.amherst.com"
gpg_home = homedir + "/.gnupg"
# optional
gpg_homeshort = "~/.gnupg"
pub_ring = gpg_home + "/pubring.gpg"
sec_ring = gpg_home + "/secring.gpg"
pring = []
sring = []
pring.append(pub_ring)
sring.append(sec_ring)
