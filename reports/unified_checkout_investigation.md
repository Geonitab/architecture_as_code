# Unified Build & Release checkout failure analysis

## Summary
- The unified workflow started failing immediately after upgrading `actions/checkout` from v4 to v5.
- Both the Docker build job and the finalize job invoke `actions/checkout@v5`, so the regression blocks the workflow before any build steps execute.
- Checkout v5 runs on the Node.js 24 runtime and requires Actions runner version 2.327.1 or newer; older runners abort with a runtime version error. This requirement was introduced with the v5 release and is absent in v4.

## Evidence
- Workflow definition showing the upgrade to `actions/checkout@v5` in the Docker build job and the finalize job.
- Official checkout documentation noting the Node.js 24 runtime requirement and the minimum runner version (2.327.1) for v5 ([actions/checkout README](https://github.com/actions/checkout/tree/main#whats-new)).

## Recommendation
- Update the self-hosted runners that execute this workflow to Actions runner >= 2.327.1 so they support Node.js 24.
- If updating the runner fleet is not immediately possible, pin the workflow back to `actions/checkout@v4` until compatible infrastructure is available.
