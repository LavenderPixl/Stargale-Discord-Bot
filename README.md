## Stargale 
Stargale is a Discord Bot made in Python for Honkai players!

Use Stargale to view Honkai players' profiles, and their featured characters, as well as their stats!
 
 Stargale can also send you a direct link to a characters Prydwen page. 
( *https://prydwen.gg* )
## Deployment

To run this project:

```bash
  docker compose up --build
```
## Environment Variables

To run this project, you will need to add the bot token into your .env file

`DISCORD_TOKEN`

### Commands

- /prydwen - Sends a link to Prydwen.
- /character - Sends a link to the specific characters profile on Prydwen; Requires characters' name.
- /help_sg - Displays all available commands.
- /profile - Displays User profile; Requires their Honkai UID.

