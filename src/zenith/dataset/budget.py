from .record_table import RecordTable


class Budget(RecordTable):
    def __init__(self, name="MyBudget", alias="Bud"):
        super().__init__(name=name, alias=alias)

        # ------------- specifics attributes ------------- #
        self.total_revenue = None
        self.total_expenses = None
        self.total_net = None
        self.summary_ascend = False

    def _set_fields(self):
        """Set fields names.
        Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()
        # set temporary util fields
        self.sign_field = "Sign"
        self.value_signed = "Value_Signed"
        # ... continues in downstream objects ... #

    def _set_data_columns(self):
        """Set specifics data columns names.
        Base Dummy Method. Expected to be incremented in superior methods.

        """
        # Main data columns
        self.columns_data_main = [
            "Type",
            "Status",
            "Contract",
            "Name",
            "Value",
        ]
        # Extra data columns
        self.columns_data_extra = [
            # Status extra
            "Date_Due",
            "Date_Exe",
            # Name extra
            # tags
            "Tags",
            # Values extra
            # Payment details
            "Method",
            "Protocol",
        ]
        # File columns
        self.columns_data_files = [
            "File_Receipt",
            "File_Invoice",
            "File_NF",
        ]
        # concat all lists
        self.columns_data = (
            self.columns_data_main + self.columns_data_extra + self.columns_data_files
        )

        # variations
        self.columns_data_status = self.columns_data_main + [
            self.columns_data_extra[0],
            self.columns_data_extra[1],
        ]

        # ... continues in downstream objects ... #

    def _set_operator(self):
        """Private method for Budget operator

        :return: None
        :rtype: None
        """

        # ------------- define sub routines here ------------- #
        def func_file_status():
            return FileSys.check_file_status(files=self.data["File"].values)

        def func_update_status():
            # filter relevante data
            df = self.data[["Status", "Method", "Date_Due"]].copy()
            # Convert 'Date_Due' to datetime format
            df["Date_Due"] = pd.to_datetime(self.data["Date_Due"])
            # Get the current date
            current_dt = datetime.datetime.now()

            # Update 'Status' for records with 'Automatic' method and 'Expected' status_t1 based on the condition
            condition = (
                (df["Method"] == "Automatic")
                & (df["Status"] == "Expected")
                & (df["Date_Due"] <= current_dt)
            )
            df.loc[condition, "Status"] = "Executed"

            # return values
            return df["Status"].values

        # todo implement all operations
        # ---------------- the operator ---------------- #

        self.operator = {
            "Status": func_update_status,
        }

    def _get_total_expenses(self, filter=True):
        filtered_df = self._filter_prospected_cancelled() if filter else self.data
        _n = filtered_df[filtered_df["Type"] == "Expense"]["Value_Signed"].sum()
        return round(_n, 3)

    def _get_total_revenue(self, filter=True):
        filtered_df = self._filter_prospected_cancelled() if filter else self.data
        _n = filtered_df[filtered_df["Type"] == "Revenue"]["Value_Signed"].sum()
        return round(_n, 3)

    def _filter_prospected_cancelled(self):
        return self.data[
            (self.data["Status"] != "Prospected") & (self.data["Status"] != "Cancelled")
        ]

    def update(self):
        super().update()
        if self.data is not None:
            self.total_revenue = self._get_total_revenue(filter=True)
            self.total_expenses = self._get_total_expenses(filter=True)
            self.total_net = self.total_revenue + self.total_expenses
            if self.total_net > 0:
                self.summary_ascend = False
            else:
                self.summary_ascend = True

        # ... continues in downstream objects ... #
        return None

    def set_data(self, input_df):
        """Set RecordTable data from incoming dataframe.
        Expected to be incremented downstream.

        :param input_df: incoming dataframe
        :type input_df: dataframe
        :return: None
        :rtype: None
        """
        super().set_data(input_df=input_df)
        # convert to numeric
        self.data["Value"] = pd.to_numeric(self.data["Value"])
        # compute temporary field

        # sign and value_signed
        self.data["Sign"] = self.data["Type"].apply(
            lambda x: 1 if x == "Revenue" else -1
        )
        self.data["Value_Signed"] = self.data["Sign"] * self.data["Value"]

    @staticmethod
    def parse_annual_budget(self, year, budget_df, freq_field="Freq"):
        start_date = "{}-01-01".format(year)
        end_date = "{}-01-01".format(int(year) + 1)

        annual_budget = pd.DataFrame()

        for _, row in budget_df.iterrows():
            # Generate date range based on frequency
            dates = pd.date_range(start=start_date, end=end_date, freq=row["Freq"])

            # Replicate the row for each date
            replicated_data = pd.DataFrame(
                {col: [row[col]] * len(dates) for col in df.columns}
            )
            replicated_data["Date"] = dates

            # Append to the expanded budget
            annual_budget = pd.concat(
                [annual_budget, replicated_data], ignore_index=True
            )

        return annual_budget

    def get_summary_by_type(self):
        summary = pd.DataFrame(
            {
                "Total_Expenses": [self.total_expenses],
                "Total_Revenue": [self.total_revenue],
                "Total_Net": [self.total_net],
            }
        )
        summary = summary.apply(
            lambda x: x.sort_values(ascending=self.summary_ascend), axis=1
        )
        return summary

    def get_summary_by_status(self, filter=True):
        filtered_df = self._filter_prospected_cancelled() if filter else self.data
        return (
            filtered_df.groupby("Status")["Value_Signed"]
            .sum()
            .sort_values(ascending=self.summary_ascend)
        )

    def get_summary_by_contract(self, filter=True):
        filtered_df = self._filter_prospected_cancelled() if filter else self.data
        return (
            filtered_df.groupby("Contract")["Value_Signed"]
            .sum()
            .sort_values(ascending=self.summary_ascend)
        )

    def get_summary_by_tags(self, filter=True):
        filtered_df = self._filter_prospected_cancelled() if filter else self.data
        tags_summary = (
            filtered_df.groupby("Tags")["Value_Signed"]
            .sum()
            .sort_values(ascending=self.summary_ascend)
        )
        tags_summary = tags_summary.sort()
        separate_tags_summary = (
            filtered_df["Tags"].str.split(expand=True).stack().value_counts()
        )
        print(type(separate_tags_summary))
        return tags_summary, separate_tags_summary

