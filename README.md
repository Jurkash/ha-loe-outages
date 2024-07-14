![HA LOE Outages Logo](./icons/logo.svg) 

# 🔌 HA LOE Outages

[![GitHub Release][gh-release-image]][gh-release-url]
[![GitHub Downloads][gh-downloads-image]][gh-downloads-url]
[![hacs][hacs-image]][hacs-url]
[![GitHub Sponsors][gh-sponsors-image]][gh-sponsors-url]
[![Patreon][patreon-image]][patreon-url]
[![Buy Me A Coffee][buymeacoffee-image]][buymeacoffee-url]
[![Twitter][twitter-image]][twitter-url]

Inspired by [ha-yasno-outages](https://github.com/denysdovhan/ha-yasno-outages)

> A Home Assistant integration for monitoring electricity outage schedules by [LOE][loe].

This integration for [Home Assistant][home-assistant] offers real-time information on planned electricity outages by [LOE][loe]. It includes a calendar of planned outages, time sensors for the next scheduled outages, and more.

**💡 Note:** This project is independently developed and is not affiliated with [LOE][loe]. The information provided may differ from their official announcements.

## Sponsorship

Your support helps maintain and develop projects like this one. Show your love and support through any of the following:

- ☕️ [Buy Me A Coffee][buymeacoffee-url]
- 🤝 [Support on Patreon][patreon-url]
- 💖 [Sponsor on GitHub][gh-sponsors-url]

## Installation

The easiest way to install this integration is via [HACS][hacs-url]. Click the button below to add it:

[![Add to HACS via My Home Assistant][hacs-install-image]][hasc-install-url]

If the button doesn't work, follow these steps to add the repository manually:

1. Go to **HACS** → **Integrations** → **...** (top right) → **Custom repositories**
2. Click **Add**
3. Enter `https://github.com/jurkash/ha-loe-outages` in the **URL** field
4. Choose **Integration** as the **Category**
5. **LOE Outages** will appear in the list of available integrations. Install it as usual.

## License

MIT © [Yurii Shunkin][jurkash]

<!-- Badges -->
[gh-release-url]: https://github.com/jurkash/ha-loe-outages/releases/latest
[gh-release-image]: https://img.shields.io/github/v/release/jurkash/ha-loe-outages?style=flat-square
[gh-downloads-url]: https://github.com/jurkash/ha-loe-outages/releases
[gh-downloads-image]: https://img.shields.io/github/downloads/jurkash/ha-loe-outages/total?style=flat-square
[hacs-url]: https://github.com/hacs/integration
[hacs-image]: https://img.shields.io/badge/hacs-default-orange.svg?style=flat-square
[gh-sponsors-url]: https://github.com/sponsors/jurkash
[gh-sponsors-image]: https://img.shields.io/github/sponsors/jurkash?style=flat-square
[patreon-url]: https://patreon.com/jurkash
[patreon-image]: https://img.shields.io/badge/support-patreon-F96854.svg?style=flat-square
[buymeacoffee-url]: https://buymeacoffee.com/jurkash
[buymeacoffee-image]: https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square
[twitter-url]: https://twitter.com/jurkashok
[twitter-image]: https://img.shields.io/badge/twitter-%40jurkashok-00ACEE.svg?style=flat-square

<!-- References -->
[loe]: https://poweron.loe.lviv.ua/
[home-assistant]: https://www.home-assistant.io/
[jurkash]: https://github.com/jurkash
[hasc-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=jurkash&repository=ha-loe-outages&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
[add-translation]: https://github.com/jurkash/ha-loe-outages/blob/master/contributing.md#how-to-add-translation
[calendar-card]: https://www.home-assistant.io/dashboards/calendar/
