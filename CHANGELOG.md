# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.1.2] - 2021-02-26
### Added
- Included `datajoint-matlab` `3.4.X` documentation. PR #257
- Version tracking of `common` docs. PR #257
- Created a changelog. PR #257
- Added `build` and `dev` docker environments. PR #257
- Added CI/CD with GitHub Actions. (#258) PR #257
- Added `docker-compose.yaml` to ignored files in git tracking to allow for local customization. PR #257
- Enhanced repo reference directory and HTML build target directories to be configurable via environment variables. PR #257

### Changed
- Modified the base docker image to be based from datajoint image tier (`djbase`). PR #257

### Removed
- `local-docker-compose.yml` environment. PR #257
- `entrypoint.sh` which is now unnecessary for the image. PR #257

[0.1.2]: https://github.com/datajoint/datajoint-docs/releases/tag/0.1.2
