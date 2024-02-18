# **Bing Image Creator DALL-E 3**
<p align="center">
  <img src="https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/74131092-2cba-4ee5-ab17-7c7ca20fccd3" alt="Banner"/>
</p>
<p align="center">
  <em>Batch generate images with Bing Image Creator (powered by DALL-E 3) using Seleniumbase.   </em>
</p>
<p align="center">
<a target="_blank" href="https://colab.research.google.com/github/meap158/bing_image_creator_dalle3_batch/blob/main/bing_image_creator_dalle3_batch_meap158.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
</p>
Bing Image Creator DALL-E 3 allows you to pull prompts directly from Google Sheets,
generate images with DALL-E 3 in Copilot Designer,
and save them directly to your Google Drive.

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
   
![image](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/42ce0b74-94e0-4b70-a492-cabc7fb8e73a)

---
### **Okay now I have the `_U` cookie, where do I put it?**
#### *Option 1. For single cookie use:*
1. Just input your `_U` cookie value into the `bing_cookie` parameter.

![image](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/9d5e5e6b-5cdf-4f9a-8f6a-65ae5e0e28e5)


#### *Option 2. For multi-cookie use (i.e., multiple accounts):*

1. Create a Secret named `bing_cookies_yaml` in the Secrets tab (the one with the key icon):

![Screenshot 2024-02-18 163003](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/d0eeac10-d2ff-4e3b-a8ae-7ac23397facf)

2. Input your `_U` cookie value(s) into the Value column following this syntax (the names on the left side don't matter much as they're just for readability. You could just put the names of your accounts there):
    ```
    account1: {_U cookie value}

    account2: {_U cookie value}
    ```
3. Enable Notebook access to the Secret.
After this step, it should look something like this:

![secret](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/062a9e57-ca73-4fed-ac1c-cd682819e422)

---
### **How to Use**
1. Fill in the necessary parameters: `spreadsheet_id`, `worksheet_name_or_index`, and `range_value`, as per your Google Sheets setup. The values from this specified range will be fetched and used as prompts.

![image](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/add604d5-2a30-4774-95ac-2030c71b6951)
2. Press `Ctrl + F9` to run all cells.

---
### **Results**
![image](https://github.com/meap158/bing_image_creator_dalle3_batch/assets/14327094/3a8169c8-1eb6-48fe-9403-dfa08670c7d4)
