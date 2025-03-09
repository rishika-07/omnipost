# OMNIPOST
A superb app to manage all your social media applications

### Suggestions for the App
Feel free to add more.
- Schedule Posts: schedule posts in a future time

### Target Applications
The app would try to cover the following social media platforms:
1. Instagram
2. Facebook
3. Twitter
4. LinkedIn
5. Telegram
6. Pinterest
7. Whatsapp community
8. Reddit
9. Quora
10. Threads
11. Youtube

## Architecture
A proposed architecture for the app is to have the following models:
- **Platform**: A model to define the configs and actions of a particular platform. It would include the following fields:
    - **configs**: A list of fields required to connect to an app, say, access token, user_id, etc.
    - **actions**: Key-value pairs of `<action>:[<commands>]`.

        An *action* is something that can be done on that platform (like creating a post).

        *Commands* are a list of commands that must be executed to perform that action. *Why a list of commands?* Because an app might require multiple steps to do that action

        Every app must have a set of commands to execute the following three actions: 
        - `post`: *create a simple post (combination of text and media)*
        - `post_short_video`: *create a short form video (such as reels)*
        - `post_story`: *create a story*


Whiteboard note:
![Architecture Diagram](/docs/images/archi.jpeg) [Architecture Diagram](/docs/images/archi.jpeg)
