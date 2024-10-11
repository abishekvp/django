Here’s a `README.md` file for your Terraform provider plugin that fetches account data from your product using `authtoken` and `server_url`.

---

# Securden Terraform Provider

The `securden` provider for Terraform allows users to securely fetch account data, such as passwords or other credentials, from the Securden server using authentication tokens and product API.

## Requirements

- Terraform version >= 0.13
- Securden credentials (authentication token) and server URL

## Installation

To install this provider, include it in your Terraform configuration as shown below. Terraform will automatically download the provider when you run the `terraform init` command.

```hcl
terraform {
  required_providers {
    securden = {
      source = "securden/securden"
    }
  }
}
```

## Provider Configuration

You need to configure the `securden` provider by specifying an `authtoken` and the `server_url` of your Securden product. These values can be provided directly or through Terraform variables.

Example:

```hcl
provider "securden" {
  authtoken  = var.authtoken
  server_url = var.server_url
}
```

You can declare these values as variables in a separate file (e.g., `terraform.tfvars`):

```hcl
# terraform.tfvars
authtoken  = "your_secure_authtoken"
server_url = "https://your-server-url"
```

Or, declare them directly in your configuration as inputs:

```hcl
variable "authtoken" {
  description = "Securden authentication token"
  type        = string
}

variable "server_url" {
  description = "Securden server URL"
  type        = string
}
```

## Fetching Account Data

Use the `securden_keyvalue` data source to fetch account data from your Securden product. You need to provide the `account_id` as an input to the data source, and the data fetched (like passwords or other credentials) can be used in your Terraform configuration.

Example:

```hcl
data "securden_keyvalue" "account_data" {
  account_id = 2000000004406
}

output "password" {
  value = data.securden_keyvalue.account_data.password
}
```

In this example:
- `account_id` is the unique identifier for the account whose data you want to retrieve.
- `data.securden_keyvalue.account_data.password` retrieves the password associated with the account ID.

### Example Usage

Below is a full example of how to use the Securden provider and data source in your Terraform configuration:

```hcl
terraform {
  required_providers {
    securden = {
      source = "securden/securden"
    }
  }
}

provider "securden" {
  authtoken  = var.authtoken
  server_url = var.server_url
}

data "securden_keyvalue" "account_data" {
  account_id = 2000000004406
}

output "password" {
  value = data.securden_keyvalue.account_data.password
}
```

### Variables Example

You can define your variables in `variables.tf` as follows:

```hcl
variable "authtoken" {
  description = "Securden authentication token"
  type        = string
}

variable "server_url" {
  description = "Securden server URL"
  type        = string
}

variable "account_id" {
  description = "Account ID to fetch data"
  type        = number
}
```

And then define their values in `terraform.tfvars`:

```hcl
authtoken  = "your_authtoken"
server_url = "https://your-securden-server-url"
account_id = 2000000004406
```

### Running Terraform

1. Initialize the provider:
   ```bash
   terraform init
   ```

2. Apply the Terraform configuration:
   ```bash
   terraform apply
   ```

## Outputs

- `password`: This output will show the password or other credentials associated with the provided `account_id` after fetching from the Securden server.

## License

This provider is licensed under the MPL-2.0 License. See the LICENSE file for more details.

---

This `README.md` covers the basic usage of your custom Terraform provider, including how to configure and use the `securden_keyvalue` data source. You can customize it further depending on the specific features or outputs your provider supports.