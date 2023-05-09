import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'
import adapterStatic from '@sveltejs/adapter-static';

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapterStatic()
  }
}
