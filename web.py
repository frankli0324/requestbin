from requestbin import config
import os

import requestbin

if __name__ == "__main__":
    port = int(os.environ.get('PORT', config.PORT_NUMBER))
    requestbin.app.run(host='0.0.0.0', port=port, debug=config.DEBUG)