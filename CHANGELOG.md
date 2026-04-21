## [1.0.4](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/compare/v1.0.3...v1.0.4) (2026-04-21)


### Bug Fixes

* replace tasks.loop with asyncio scheduler for DST-safe nightly backup ([f238232](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/f238232123f02fb138dd59ab746a9cb7575e9b7f))
* resolve nightly backup task silently dying due to ZoneInfo TypeError ([df53d11](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/df53d11c075d58045457ac619010a54d01e3c8af))

## [1.0.4](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/compare/v1.0.3...v1.0.4) (2026-04-21)


### Bug Fixes

* replace tasks.loop with asyncio scheduler for DST-safe nightly backup ([f238232](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/f238232123f02fb138dd59ab746a9cb7575e9b7f))
* resolve nightly backup task silently dying due to ZoneInfo TypeError ([df53d11](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/df53d11c075d58045457ac619010a54d01e3c8af))

## [1.0.3](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/compare/v1.0.2...v1.0.3) (2026-03-29)


### Bug Fixes

* update deployment health check from port 8000 to 9191 ([e6c5925](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e6c592502be7d83325b028b02d43735438104a7e))

## [1.0.2](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/compare/v1.0.1...v1.0.2) (2026-03-29)


### Bug Fixes

* use __version__ instead of hardcoded version string in main.py ([bdf191e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/bdf191e3c140659674da3cd375514be9b3efc627))

## [1.0.1](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/compare/v1.0.0...v1.0.1) (2026-03-29)


### Bug Fixes

* remove UvicornIntegration removed in sentry-sdk 2.x ([7d9cacb](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7d9cacb9e7edb2cb4c3876ccb06b6be43cc45f19))
* wire API host/port through settings to resolve SonarQube S8392 ([a255c04](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/a255c0450fbd928734488ca5fc400492a79d2c49))

# 1.0.0 (2026-03-29)


### Bug Fixes

* add .js extension to semantic-release plugin path ([9ee001d](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/9ee001d6666743661e0e338c0f2d7bceb7ef5c3d))
* add error handling for missing project in automation workflows ([855c17e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/855c17ee095682599c3dc91538ab09b6591ea4e8))
* **back merge:** add debug to why creating PR is failing ([b431479](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/b43147982efa5f01a51d87efb981a40b9bfce14c))
* **back merge:** add debug to why creating PR is failing ([#74](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/74)) ([2463b9f](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2463b9fc80542d412ad9a78b4a1db17955fc372a))
* **back merge:** finalize changes for being able to back merge main i… ([#76](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/76)) ([2242ffc](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2242ffc2e7d80ae0682a763fa7daa007decff0bd))
* **back merge:** finalize changes for being able to back merge main into develop ([dbe572f](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/dbe572f61fbb4efa0e44cdaab4e113c9fd109e11))
* **back-merge:** fix back-merge ([179bef2](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/179bef2cfc63fe2aba1e14ceedd708dccb836ef8))
* **bugfix:** fix broken package lockfile ([75fd0ef](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/75fd0efd720e3e12b37e049c62362226e88421c7))
* **bugfix:** fix broken package lockfile ([#55](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/55)) ([7380c0d](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7380c0d3af8e29a49129079ca3c2afc1de414d9e))
* **chatinputcommandsuccess.spec.ts:** resolve jest module mapping issue ([621621c](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/621621cbfc57878bf580e7471641db8c490d8d9a)), closes [#110](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/110)
* **chatinputcommandsuccess.spec.ts:** resolve jest module mapping issue ([#198](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/198)) ([e4eb9e1](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e4eb9e1004aaff4f2b32b584851ac8e51aaae01f))
* check .env file exists before loading in production ([3f1e0b1](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/3f1e0b1e80538e837f79384ecc72f0e6e03fe24c))
* **ci:** add SENTRY_DSN environment variable to testing workflow ([#228](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/228)) ([938442d](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/938442d1f78f3babdfced1b8a31c882abeb9b94d))
* **ci:** add SENTRY_DSN environment variable to testing workflow ([#228](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/228)) ([#229](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/229)) ([b0acb7e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/b0acb7e1c5117a406b89bff978bc4ad1adb3b632))
* **code coverage:** resolve SonarQube code coverage error ([#96](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/96)) ([9b15a40](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/9b15a40a048ca0da10657e8f04656531e28843fd))
* **code coverage:** resolve SonarQube code coverage errro ([d923a51](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/d923a510dad71e6007a6523cb623a7ad341abfe6))
* correct GitHub Actions expression syntax for PROJECT_NUMBER variable ([9f4342e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/9f4342ea537986e70a117b680d612ca1eef19af5))
* exclude test files from SonarQube source analysis ([e5dc782](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e5dc78261fea2ad8308e49cafdba05f5a5ba661e))
* load .env as base before .env.production in production ([dcd8b23](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/dcd8b235f84b2e628612a0b00cec3d5313de1b53))
* make project automation optional - skip gracefully if project doesn't exist ([2fa2313](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2fa2313dc25ca00f16c6b9e0226403170403ba63))
* only load .env.production in production, skip .env ([dff85e2](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/dff85e2c683ee6983ad6f74e27ee82cb95f7edcf))
* **package:** update packages to fix builds ([c24a458](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/c24a458b05e3871083e75927be3d4848891bff58))
* remove explicit ref from checkout to use default PR behavior ([#216](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/216)) ([a164594](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/a1645941c94b319b04b8225e70b196e7134755e9))
* remove invalid GitHub Actions expression syntax for PROJECT_NUMBER default ([e00b03b](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e00b03b6504ef47ec83a21f98db487160ad1a620))
* remove invalid GitHub Actions expression syntax for PROJECT_NUMBER default ([e4c564c](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e4c564cfa96906e74261df33cee419b230ccf7b7))
* remove trailing whitespace in project-automation.yml ([8f15509](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/8f15509f69ebf818291cd812dd359f907d3b8edc))
* remove unnecessary async keyword from verify_api_key ([08e3a2a](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/08e3a2a0f7c05726bb75cfb1a2aca290452ab24f))
* resolve YAML syntax error in project-automation workflow ([e2eda76](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e2eda7672b6be33cbf21a39a8fd96fec5665e727))
* restrict CodeQL analysis to PRs targeting develop only ([d9bbff8](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/d9bbff8a171ed8829ed6d11903dd400b4069d0d7))
* schedule backup using America/New_York timezone to handle DST ([b1c01ca](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/b1c01caa4886c3841ce1d4feb15a1e9d60f2c215))
* schedule nightly backup in UTC to prevent DST drift ([277a21f](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/277a21f6dc7fe20947b13d45ce823d393ff834f1))
* **security checks:** resolve hung merge request ([39c2b3e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/39c2b3efd4ba19b222840fb88252f649c07f5a01))
* update CI workflow to test feature branches instead of target branch ([#215](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/215)) ([15de2e9](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/15de2e9a6be690ab6e3cc59794900f0b8cdb295f))
* update project-automation.yml to match working version from NightScoutMongoBackupSite ([895971b](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/895971b46354da63123adbf33a671eac6ea385ec))
* Update SonarCloud action to use sonarqube-scan-action ([#387](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/387)) ([da89500](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/da89500ef875ba74997b30882b44099ab7e3790b))
* use resolved absolute paths for load_dotenv calls ([7f96446](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7f96446c8f6e4ae8e687544238477b42a61082ff))
* **utils.spec.ts:** resolve remaining jest module mapping issue ([2a605d7](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2a605d79e51c1a6797105760bee697873807b2c9)), closes [#110](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/110)
* **utils.spec.ts:** resolve remaining jest module mapping issue ([#199](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/199)) ([0b996c8](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/0b996c8b51d6791636986bfe31c3192883c19e11))
* **workflow:** attempt to resolve testing workflow errors with bot token ([7841dd6](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7841dd624121b63b58002ae1c4040fe7b1039308))
* **workflow:** attempt to resolve testing workflow errors with bot token ([#99](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/99)) ([2dcdb75](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2dcdb755eb20d37c0576d0bb973c9585c6091951))


### Features

* Add automatic sync workflow from main to develop ([#249](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/249)) ([99c08eb](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/99c08eb583eff1f38c430a73316941c372b9b4a2))
* add missing utils.ts file with logSuccessCommand and getSuccessLoggerData functions ([b22ac87](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/b22ac8794ba4afc721fb9bf049696b37bc667c14))
* **add query db command with associated  files.:** /querydb command was added with unit testing ([e608483](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e60848344574e5a8f03015605f3148b537c042fe)), closes [#110](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/110)
* **add query db command with associated  files.:** /querydb command was added with unit testing ([#194](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/194)) ([c5a75d7](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/c5a75d78759818b2247ec6ad4eaf21e45fbc4b2a))
* add semantic versioning for bot and API ([844dde2](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/844dde2680e44cfb7f85653e9f9e0648dccf1e83))
* add support for .env.production file ([2f4af4c](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2f4af4c080d55107f0efccb9d3b2e30f21a7a980))
* **backup:** backup commands ([#227](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/227)) ([63c8fec](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/63c8fec713cf572b7b07743f1cfab42748af4ec2))
* **bot:** establish initial Discord bot connection ([ee7774e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/ee7774ee6ee03710868bfa9a530b1bbb67e539d6)), closes [#7](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/7)
* **bot:** establish initial Discord bot connection ([#29](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/29)) ([6a20185](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/6a201853f3eb9f2398b150da39ec1aca881d46af))
* **code coverage:** add code coverage ([7631f2e](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7631f2e9cab32b378f0bd58517ed56df7b641ca4))
* **code coverage:** add code coverage ([#33](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/33)) ([212f3fc](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/212f3fc3f097c15c9d2db9dba71d4c3c5500f3c4))
* **command:** add ping command and test ([1d95835](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/1d958359515cb2ed2605dc7d3762ed4c0595c9e2))
* **command:** add ping command and test ([#94](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/94)) ([98f55b6](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/98f55b608c14575317d33b9da946796c5f8dc1a1))
* **core files:** add core files for bot ([6b1401a](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/6b1401a178343c1fe9db95183abf46cdef90cf3c)), closes [#197](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/197)
* **core files:** add core files for bot ([#208](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/208)) ([77c66b3](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/77c66b34c7bd67b55a40e5d634641655c3d194b7))
* improve project lookup with available projects listing ([e6b08d7](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/e6b08d7258022391c089d99f990670761d8e1fc0))
* **issues:** import SonarQube issues to GitHub ([1ea7f53](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/1ea7f5346670a19ce6cc23416c2e78acec002c50))
* **issues:** import SonarQube issues to GitHub ([#54](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/54)) ([bfca306](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/bfca30676096a0c5215c8fee0d6ff08c30263071))
* **logging:** add Sentry for error logging and associated tests ([61dc63a](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/61dc63a23d2aaa3015feb707b27fe067076a8ace))
* **logging:** add Sentry for error logging and associated tests ([#43](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/43)) ([d40a053](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/d40a05368b5efd882afb7ff58502a9c78d72069d))
* remove deprecated Dependabot reviewers config and add CODEOWNERS ([#217](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/217)) ([62edd51](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/62edd51ece2dccefe32f3b453abbefc120359b89))
* **scans:** add semgrep scan to workflow ([cf401b9](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/cf401b99e68c4348b44357095efb442bc3668cfb))
* **scans:** add semgrep scan to workflow ([#87](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/87)) ([2eef0db](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/2eef0dbdc73d8a691d56fda9f67f17d2c196f96a))
* **schedule:** have issues pulled from SonarQube every 15 minutes ([7d44b2a](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/7d44b2adc72b4857bcc2a89bd9cfe2bae78e8d09))
* **schedule:** have issues pulled from SonarQube every 15 minutes ([#57](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/issues/57)) ([f2f8e89](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/f2f8e89227b00687173ff90c400c0b062929cae8))


### Reverts

* Revert "🔵 other: Add workflow to delete branches after merging" ([1211dda](https://github.com/Stelth2000-Inc/NightScoutMongoBackup/commit/1211ddabd9a7cb26c425a426e0f88908aab7ccdb))
