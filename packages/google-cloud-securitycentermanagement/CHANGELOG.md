# Changelog

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.8...google-cloud-securitycentermanagement-v0.1.9) (2024-05-27)


### Features

* add support for new Security Center Management APIs ([9896255](https://github.com/googleapis/google-cloud-python/commit/98962551bbe4c8901950a9769c7d5fd4369f2ef5))


### Documentation

* update comment formatting throughout API ([9896255](https://github.com/googleapis/google-cloud-python/commit/98962551bbe4c8901950a9769c7d5fd4369f2ef5))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.7...google-cloud-securitycentermanagement-v0.1.8) (2024-03-22)


### Bug Fixes

* annotate EffectiveEventThreatDetectionCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate EffectiveSecurityHealthAnalyticsCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate EventThreatDetectionCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate SecurityHealthAnalyticsCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))


### Documentation

* updated comments ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.6...google-cloud-securitycentermanagement-v0.1.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0  ([add6a6d](https://github.com/googleapis/google-cloud-python/commit/add6a6d5198c81e35e5edf8997eb9fde2cc9c81b))


### Documentation

* Clarify documentation for ListDescendantSecurityHealthAnalyticsCustomModules RPC and CustomConfig message ([add6a6d](https://github.com/googleapis/google-cloud-python/commit/add6a6d5198c81e35e5edf8997eb9fde2cc9c81b))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.5...google-cloud-securitycentermanagement-v0.1.6) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([89c1b05](https://github.com/googleapis/google-cloud-python/commit/89c1b054f321b90ab4eed0139a3a2a79c369730d))


### Documentation

* [google-cloud-securitycentermanagement] Finish a sentence with a period ([#12300](https://github.com/googleapis/google-cloud-python/issues/12300)) ([833998a](https://github.com/googleapis/google-cloud-python/commit/833998a27193f6d9c95d054a352702439c596165))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.4...google-cloud-securitycentermanagement-v0.1.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.3...google-cloud-securitycentermanagement-v0.1.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12243](https://github.com/googleapis/google-cloud-python/issues/12243)) ([e14d4b1](https://github.com/googleapis/google-cloud-python/commit/e14d4b13a883876a420c498a044dc34ea5122629))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.2...google-cloud-securitycentermanagement-v0.1.3) (2024-01-19)


### Documentation

* [google-cloud-securitycentermanagement] update documentation for UpdateSecurityHealthAnalyticsCustomModule update_mask field ([#12196](https://github.com/googleapis/google-cloud-python/issues/12196)) ([c7cf0a1](https://github.com/googleapis/google-cloud-python/commit/c7cf0a1c754091fb5b141dd7a9238c63f9d1f36e))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.1...google-cloud-securitycentermanagement-v0.1.2) (2024-01-08)


### Documentation

* [google-cloud-securitycentermanagement] updates on multiple comments, syncing terminology and clarifying some aspects ([#12151](https://github.com/googleapis/google-cloud-python/issues/12151)) ([461c76b](https://github.com/googleapis/google-cloud-python/commit/461c76bbc6bd7cda3ef6da0a0ec7e2418c1532aa))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.0...google-cloud-securitycentermanagement-v0.1.1) (2024-01-04)


### Documentation

* [google-cloud-securitycentermanagement] clarify several RPC descriptions ([#12146](https://github.com/googleapis/google-cloud-python/issues/12146)) ([a7e4920](https://github.com/googleapis/google-cloud-python/commit/a7e492084f88c72d77127d6adf9feb537362ca18))

## 0.1.0 (2023-12-07)


### Features

* add initial files for google.cloud.securitycentermanagement.v1 ([#12089](https://github.com/googleapis/google-cloud-python/issues/12089)) ([48e7c5f](https://github.com/googleapis/google-cloud-python/commit/48e7c5f9b3747f7ccf85733a99666a3df7206c94))

## Changelog
