# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.2.4] - 2023-07-12

### Fix

- Remove archive note since `datajoint-matlab` legacy docs will remain live PR #281

## [0.2.3] - 2022-10-10

### Added

- Archiving note PR #280

### Fix

- Correct part table force note PR #279

## [0.2.2] - 2022-06-13

### Added

- Add instructions on how to disable checksums for filepath external data PR #277

### Changed

- Include example for sorting `dj.kill` command. (#237) PR #238
- Update list of available builtin functions in query aggregation. (#253) PR #268

## [0.2.1] - 2021-07-14

### Changed

- Modify the TLD of docs site from `docs.datajoint.io` -> `docs.datajoint.org`. PR #266

## [0.2.0] - 2021-03-24

### Added

- Add `update1` documentation and reference it properly to datajoint-python, release 0.13. PR #264
- Add `query_caching` documentation and reference it properly to datajoint-python, release 0.13. PR #264
- Add transpiler design documentation and reference it properly to datajoint-python, release 0.13. PR #264

### Changed

- Modify the markdown parsing to `m2r2` and allow content to be included. PR #264
- Update reverse proxy image from `datajoint` org. PR #264

## [0.1.5] - 2021-03-11

### Added

- Numbering for easy reference in `Contribute` section. PR #262

## [0.1.4] - 2021-03-01

### Added

- Added `Community` section. PR #259
- Added previously discussed contribution guidelines document in `Community > Contribute`. (#260) PR #259

### Changed

- Moved `Introduction > Publications` to `Community > Publications` section. PR #259.
- Moved `Introduction > Community` to `Community > Engagements` section. PR #259.

### Removed

- `Introduction > Contribute`. PR #259
- `Introduction > Issues`. PR #259

## [0.1.3] - 2021-02-26

### Added

- Included `datajoint-matlab` `3.4.X` documentation. PR #257
- Version tracking of `common` docs. PR #257
- Created a changelog. PR #257
- Added `build` and `dev` docker environments. PR #257
- Added CI/CD with GitHub Actions. (#258) PR #257, #261
- Added `docker-compose.yaml` to ignored files in git tracking to allow for local customization. PR #257
- Enhanced repo reference directory and HTML build target directories to be configurable via environment variables. PR #257

### Changed

- Modified the base docker image to be based from datajoint image tier (`djbase`). PR #257

### Removed

- `local-docker-compose.yml` environment. PR #257
- `entrypoint.sh` which is now unnecessary for the image. PR #257

[0.2.4]: https://github.com/datajoint/datajoint-docs/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/datajoint/datajoint-docs/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/datajoint/datajoint-docs/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/datajoint/datajoint-docs/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/datajoint/datajoint-docs/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/datajoint/datajoint-docs/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/datajoint/datajoint-docs/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/datajoint/datajoint-docs/releases/tag/v0.1.3
