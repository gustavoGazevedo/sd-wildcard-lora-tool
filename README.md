# SD wildcard lora tool

Script to generate wildcards based on your loras.

## How to Use

1. **Install the following Extensions:**
   - [Stable Diffusion Dynamic Prompts](https://github.com/adieyal/sd-dynamic-prompts)
   - [Civitai Helper](https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper)

2. **Start automatic1111.**

3. Go to the extension tab "Civitai Helper." There is a button called "Scan model."

4. In model types, select "lora" and click "scan." This will download preview images for your Loras and a `.info` file that will contain the trigger words.

5. After this is finished, go to the `config.json` file, and:
   - Add to the whitelist the path to your Lora folder.
   - Add to the blacklist what folders to ignore.

6. Run `run.bat`, and then copy the generated files to "/path/to/stable-diffusion-webui/extensions/sd-dynamic-prompts/wildcard".

### Other Configurations:

- **subfolders:** If set to true, it will search all subfolders.
- **createWildcardForSubfolders:** If set to true, it will create a separate wildcard for each subfolder.
- **WildcardName:** The name of the wildcard text file. Subfolders will be named after their folder name.
- **minimumNumberOfCombinations:** Set to zero to get all possible trigger word variations.
- **weights:** Specify what weights are supposed to be used in the Loras. This will create `minimumNumberOfCombinations` x `number of weights`.
