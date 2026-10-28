# Caucasus Online

Editable source for the Caucasus 3D multiplayer world prototype.

## Current runtime
The first runtime is hosted by Pinian Federation so it can use same-origin Federation session cookies and WebSocket signaling:
- Pin Browser route: `caucasus.pin`
- Runtime page: `/caucasus`
- Server endpoints: `/api/caucasus/config`, `/api/caucasus/guest`, `/ws/caucasus`

## Server setup
In the Render environment for the Pinian Federation service, set `CESIUM_ION_TOKEN` to a Cesium ion access token. The server reads it from environment variables and does not hardcode it in this project. CesiumJS needs a token in the browser to request ion terrain; therefore the endpoint returns that token to the client. Use a dedicated, restricted Cesium ion token with only the required terrain/asset permissions, not an unrestricted personal token.

The game uses the existing Pinian Federation login. Register/login on the Federation portal first, then open `caucasus.pin` in Pin Browser.

## Current prototype limitations
- Player positions and recent chat messages live in server memory and reset when the service restarts; they are not stored in MongoDB.
- Voice chat uses WebRTC peer-to-peer and a public STUN server. Some networks require a TURN server.
- The Cesium terrain comes from Cesium World Terrain; the initial camera is focused on the Caucasus region.
- This folder is editable source in PinCode. The live multiplayer runtime currently uses the Federation-hosted route because the Pin Browser sandboxed preview is not suitable for same-origin WebSocket authentication.
