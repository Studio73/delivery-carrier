# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class StockImmediateTransfer(models.TransientModel):
    _inherit = ["stock.immediate.transfer", "stock.number.package.mixin"]
    _name = "stock.immediate.transfer"

    def process(self):
        if self.number_of_packages:
            self.pick_ids.write({"number_of_packages": self.number_of_packages})
        # put context key for avoiding
        # `base_delivery_carrier_label` auto-packaging feature
        res = super(
            StockImmediateTransfer, self.with_context(set_default_package=False)
        ).process()
        if self.print_package_label:
            report = (
                self.pick_ids.picking_type_id.report_number_of_packages
                or self.env.ref(
                    "delivery_package_number.action_delivery_package_number_report"
                )
            )
            report_action = report.report_action(self.pick_ids)
            report_action.update({"close_on_report_download": True})
            return report_action
        return res
