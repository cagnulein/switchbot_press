# switchbot_press

This is a simple project that manage the Switchbot ( https://amzn.to/3dnliBD ) that has only the "press" ability.
Infact, the standard Switchbot plugin that comes with HASSIO, has only the ability to turn it on or off, but it doesn't work at all with these Switchbot (different firmware i guess). 

A simple configuration could be:
```yaml
switch:
  - platform: switchbot_press
    mac: 'DD:A6:10:22:11:33'

```

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)