/**
 * Saving or clearing a key rebuilds the app under the identity provider. The next first-run guard
 * to mount is told the rebuild is not a fresh visit, so the page stays where it is.
 */
let keepRoute = false;

export const markCredentialRemount = () => { keepRoute = true; };

export const consumeCredentialRemount = () => {
    const value = keepRoute;
    keepRoute = false;
    return value;
};
