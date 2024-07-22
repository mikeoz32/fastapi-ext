# Authentication

Authentication app provides mechanisms to authenticate users with external OpenID identity providers. 
Only one provider could be configured. For `sign in with ...` functionality use providers like keycloak/Auth0 or similar with
such functionality implemented in provider side.

## Setup

To enuble application add `fastapi_ext.auth` to config.json. 

### Bearer only

This configuration allows get identity information from bearer tokens, no login/logout or any other endpoints are exposed. Tokens retreiving
should be implemented on client side.

#### Example Architecture

**Keycloak as an identity provider**

Keycloak is configured with example-app realm that have two clients:
* webapp - puclic client 
* webapi - secured client with client credentials configured

**SPA implemented with VueJS**

Single page app that uses keycloakjs to redirect to keycloak and retrieve tokens. Then uses this tokens in requests to an API

**API that uses bearer only configuration**

fastapi_ext enabled application that have private endpoints secured by bearer tokens. On each request to such endpoint app with decode 
and validate tokens and add Identity object to request

## Entites

### Identity

Represents external identity from identity provider. 
=======
Authentication is provided by integration with external OpenID service of choice.

## Configuration

Add `fastapi_ext.auth` to applications in `config.json`

# OpenID

Optional OpenID application that provides some OpenID features compatible with fastapi-ext authentication
