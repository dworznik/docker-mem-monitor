# Simple Docker container memory monitor
Runs in a container next to the application to be monitored. Monitors memory utilization and sends email alerts when memory usage exceeds the limit.
**

## Configuration
Copy the `.env.example` to `.env.${ENV}` and provide your configuration.
 1. Monitor config
 1. Alert sender and recipient email addresses
 1. AWS configuration (credentials and SES config)

## Docker
Docker Compose configuration and simple Makefile with basic operations are provided.

```bash
export ENV=development
make deploy
make logs
make stop 
```
## License
MIT: <https://dworznik.mit-license.org>
