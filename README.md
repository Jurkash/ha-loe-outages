<!-- ![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)
-->
![HA LOE Outages Logo](./icons/logo.svg) 

# ⚡️ HA LOE Outages

[![GitHub Release][gh-release-image]][gh-release-url]
[![GitHub Downloads][gh-downloads-image]][gh-downloads-url]
[![hacs][hacs-image]][hacs-url]
[![GitHub Sponsors][gh-sponsors-image]][gh-sponsors-url]
[![Patreon][patreon-image]][patreon-url]
[![Buy Me A Coffee][buymeacoffee-image]][buymeacoffee-url]
[![Twitter][twitter-image]][twitter-url]

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
3. Enter `https://github.com/jurakash/ha-loe-outages` in the **URL** field
4. Choose **Integration** as the **Category**
5. **LOE Outages** will appear in the list of available integrations. Install it as usual.

<!-- 
## Usage

This integration can be configured via the UI. On the **Devices and Services** page, click **Add Integration** and search for **LOE Outages**.

Find your group by visiting the [LOE][loe] website and entering your address in the search bar. Select your group in the configuration.

![Configuration flow](https://github.com/jurkash/ha-loe-outages/assets/3459374/e8bfde50-fcbe-45c3-b448-b451b0ac3bcd)

After configuring, add the integration to your dashboard to view the next planned outages.

![Device page](https://github.com/jurkash/ha-loe-outages/assets/3459374/df628647-fd2a-455d-9d08-0d1542b67e41)

The integration also provides a calendar view of planned outages, which can be added to your dashboard via the [Calendar card][calendar-card].

![Calendar view](https://github.com/jurkash/ha-loe-outages/assets/3459374/b09c4db3-d0a0-4e06-8dd9-3f4a59f1d63e)

Here’s an example of a dashboard using this integration:

![Dashboard example](https://github.com/jurkash/ha-loe-outages/assets/3459374/26c75595-8984-4a9f-893a-e4b6d838b7f2) -->

<!-- ## Development

Interested in contributing to the project?

First, thank you! Check out the [contributing guideline](./CONTRIBUTING.md) for more information. -->

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
