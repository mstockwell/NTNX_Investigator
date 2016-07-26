import sys
from ntnxwdw import app

if __name__ == '__main__':
    try:
        app.run(debug=False)
    except Exception as ex:
        print ex
        sys.exit(1)
