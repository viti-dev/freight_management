# Freight Management Module

## Setup
1. Install this module into your Odoo instance.
2. Create user roles:
   - `Freight Manager` for approving freight orders.
   - `Freight Staff` for creating orders.

## Workflow
- **Creating Orders:** Freight orders can be created with `Freight Type` and `Cargo Weight`.
- **Approval Process:** For high-value orders (over $500,000 or 50 tons), an approval process must be followed.
- **Reporting:** The module includes a report for freight orders, categorized by freight type and approval status.

## Security Configurations
- `Freight Managers` have full access to freight orders and approvals.
- `Freight Staff` can only create orders and cannot approve high-value orders.
