/// <reference types="vite/client" />

/** Adds TypeScript module typing for CSS imported by the Vite application. */
declare module "*.css" {
  const css: string;
  export default css;
}
