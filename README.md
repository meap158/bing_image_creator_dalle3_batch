# **Bing Image Creator DALL-E 3 Batch v1.4**
<a target="_blank" href="https://colab.research.google.com/github/meap158/bing_image_creator_dalle3_batch/blob/main/bing_image_creator_dalle3_batch.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

---

### **How to Obtain Bing Cookie**
To use Bing Image Creator, you need to obtain the necessary cookie value. Follow these steps:

1. Navigate to Bing Image Creator: https://www.bing.com/images/create.
2. Log in to your Bing account.
3. Open the browser's developer tools:
   - Press `F12` or right-click on the page and select "Inspect" or "Inspect Element."
4. In the Developer Tools, go to the "Application" tab.
5. Under "Cookies," find and select `https://www.bing.com`.
6. Look for the `_U` cookie.
7. Copy the value of the `_U` cookie.
---

### **How to Use**

1. Create a Secret named `bing_cookies_yaml` in the Secrets tab (the one with the key icon):
![Screenshot 2024-02-18 163003](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/d0eeac10-d2ff-4e3b-a8ae-7ac23397facf)
3. Input your `_U` cookie value(s) into the Value column following this syntax (the names on the left side don't matter much as they're just for readability. You could put the names of your accounts there):
    ```
    account1: {_U cookie value}

    account2: {_U cookie value}
    ```
4. Enable Notebook access to the Secret.
After this step, it should look something like this:
![secret](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/062a9e57-ca73-4fed-ac1c-cd682819e422)
5. Fill in the necessary parameters: `spreadsheet_id`, `worksheet_name_or_index`, and `range_value`, as per your Google Sheets setup. The values from this specified range will be fetched and used as prompts.
![configure_googlesheets](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/15229257-8881-4339-ba8e-aa8508f36bfd)
6. Press `Ctrl + F9` to run all cells.

---
### **Results**
![image](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/3a8169c8-1eb6-48fe-9403-dfa08670c7d4)