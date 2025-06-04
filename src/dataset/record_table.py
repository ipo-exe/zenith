from .base import DataSet


class RecordTable(DataSet):
    """The core object for Record Tables. A Record is expected to keep adding stamped records
    in order to keep track of large inventories, catalogs, etc.
    All records are expected to have a unique Id. It is considered to be a relational table.


    Import RecordTable

    .. code-block:: python

        # Import RecordTable
        from plans.src_root import RecordTable

    Instantiate RecordTable Object

    .. code-block:: python

        # Instantiate RecordTable object
        rt = RecordTable(name="RecTable_1", alias="RT1")

    Setup custom columns for the data

    .. code-block:: python

        # Setup custom columns for the data
        rt.columns_data_main = ["Name", "Size"]  # main data
        rt.columns_data_extra = ["Type"]  # extra data
        rt.columns_data_files = ["File_P"]  # file-related
        rt.columns_data = rt.columns_data_main + rt.columns_data_extra + rt.columns_data_files

    Set Object Metadata and Load Data

    .. code-block:: python

        # Set object metadata and load data.
        # Note: this dummy object expects the following columns in data
        rt.set(
            dict_setter={
                "Name": "RecTable_01",
                "Alias": "RT01",
                "Color": "red",
                "Source": "-",
                "Description": "This is RecordTable Object",
                "File_Data": "/content/data_rt1.csv"
            },
            load_data=True
        )


    Check Data

    .. code-block:: python

        # Check data `pandas.DataFrame`
        print(rt.data.head())

    Load More Data from Other File

    .. code-block:: python

        # Load more new data from other file
        rt.load_data(file_data="/content/data_rt2.csv")

    Insert New Record

    .. code-block:: python

        # Insert new record from incoming dict
        d2 = {
            "Name": "k",
            "Size": 177,
            "Type": 'input',
            "File_P": "/filee.pdf",
        }
        rt.insert_record(dict_rec=d2)

    Edit Record

    .. code-block:: python

        # Edit record based on ``RecId`` and new dict
        d = {
            "Size": 34,
            "Name": "C"
        }
        rt.edit_record(rec_id="Rec0002", dict_rec=d)

    Archive a Record

    .. code-block:: python

        # Archive a record in the RT, that is ``RecStatus`` = ``Off``
        rt.archive_record(rec_id="Rec0003")

    Get a Record Dict by ID

    .. code-block:: python

        # Get a record dict by id
        d = rt.get_record(rec_id="Rec0001")
        print(d)

    Get a Record DataFrame by ID

    .. code-block:: python

        # Get a record `pandas.DataFrame` by id
        df = rt.get_record_df(rec_id="Rec0001")
        print(df.to_string(index=False))

    Load Record Data from CSV

    .. code-block:: python

        # Load record data from a ``csv`` file to a dict
        d = rt.load_record_data(file_record_data="/content/rec_rt2.csv")
        print(d)

    Export a Record to CSV

    .. code-block:: python

        # Export a record from the table to a ``csv`` file
        f = rt.export_record(
            rec_id="Rec0001",
            folder_export="/content",
            filename="export_rt2"
        )
        print(f)


    """

    def __init__(self, name="MyRecordTable", alias="RcT"):
        # prior attributes

        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)
        # overwriters
        self.object_alias = "FS"

        # --------- defaults --------- #
        self.id_size = 4  # for zfill

        # --------- customizations --------- #
        self._set_base_columns()
        self._set_data_columns()
        self._set_operator()

        # UPDATE
        self.update()

    def _set_fields(self):
        """Set fields names.
        Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()
        # base columns fields
        self.recid_field = "RecId"
        self.rectable_field = "RecTable"
        self.rectimest_field = "RecTimestamp"
        self.recstatus_field = "RecStatus"
        # ... continues in downstream objects ... #

    def _set_base_columns(self):
        """Set base columns names.
        Base Method. Expected to be incremented in superior methods.

        """
        self.columns_base = [
            self.recid_field,
            self.rectable_field,
            self.rectimest_field,
            self.recstatus_field,
        ]
        # ... continues in downstream objects ... #

    def _set_data_columns(self):
        """Set specifics data columns names.
        Base Dummy Method. Expected to be incremented in superior methods.

        """
        # Main data columns
        self.columns_data_main = [
            "Kind",
            "Value",
        ]
        # Extra data columns
        self.columns_data_extra = [
            "Category",
        ]
        # File-related columns
        self.columns_data_files = ["File_NF", "File_Invoice"]
        # concat all lists
        self.columns_data = (
            self.columns_data_main + self.columns_data_extra + self.columns_data_files
        )
        # ... continues in downstream objects ... #

    def _set_operator(self):
        """Set the builtin operator for automatic column calculations.
        This is a Base and Dummy method. It is expected to be overwrited and implemented downstream.

        :return: None
        :rtype: None
        """

        # ------------- define sub routines here ------------- #

        def func_file_status():
            return FileSys.check_file_status(files=self.data["File"].values)

        def func_sum():
            return None

        def func_age():
            return RecordTable.running_time(
                start_datetimes=self.data["Date_Birth"], kind="human"
            )

        # ---------------- the operator ---------------- #
        self.operator = {
            "Sum": func_sum,
            "Age": func_age,
            "File_Status": func_file_status,
        }
        # remove here for downstream objects!
        self.operator = None
        return None

    def _get_organized_columns(self):
        """Return the organized columns (base + data columns)

        :return: organized columns (base + data columns)
        :rtype: list
        """
        return self.columns_base + self.columns_data

    @staticmethod
    def get_timestamp():
        """Return a string timestamp

        :return: full timestamp text %Y-%m-%d %H:%M:%S
        :rtype: str
        """
        # compute timestamp
        _now = datetime.datetime.now()
        return str(_now.strftime("%Y-%m-%d %H:%M:%S"))

    def _last_id_int(self):
        """Compute the last ID integer in the record data table.

        :return: last Id integer from the record data table.
        :rtype: int
        """
        if self.data is None:
            return 0
        else:
            df = self.data.sort_values(by=self.recid_field, ascending=True)
            return int(df[self.recid_field].values[-1].replace("Rec", ""))

    def _next_recid(self):
        """Get the next record id string based on the existing ids.

        :return: next record id
        :rtype: str
        """
        last_id_int = self._last_id_int()
        next_id = "Rec" + str(last_id_int + 1).zfill(self.id_size)
        return next_id

    def _filter_dict_rec(self, input_dict):
        """Filter input record dictionary based on the expected table data columns.

        :param input_dict: input record dictionary
        :type input_dict: dict
        :return: filtered record dictionary
        :rtype: dict
        """
        # ------ parse expected fields ------- #
        # filter expected columns
        dict_rec_filter = {}
        for k in self.columns_data:
            if k in input_dict:
                dict_rec_filter[k] = input_dict[k]
        return dict_rec_filter

    def update(self):
        super().update()
        # ... continues in downstream objects ... #
        return None

    def save(self):
        """Save the data to the sourced file data.

        .. danger::

            This method **overwrites** the sourced data file.


        :return: integer denoting succesfull save (0) or file not found (1)
        :rtype: int
        """
        if self.file_data is not None:
            # handle filename
            filename = os.path.basename(self.file_data).split(".")[0]
            # handle folder
            self.export(
                folder_export=os.path.dirname(self.file_data), filename=filename
            )
            return 0
        else:
            return 1

    def export(self, folder_export=None, filename=None, filter_archive=False):
        """Export the ``RecordTable`` data.

        :param folder_export: folder to export
        :type folder_export: str
        :param filename: file name (name alone, without file extension)
        :type filename: str
        :param filter_archive: option for exporting only records with ``RecStatus`` = ``On``
        :type filter_archive: bool
        :return: file path is export is successfull (1 otherwise)
        :rtype: str or int
        """
        if filename is None:
            filename = self.name
        # append extension
        filename = filename + ".csv"
        if self.data is not None:
            # handle folders
            if folder_export is not None:
                filepath = os.path.join(folder_export, filename)
            else:
                filepath = os.path.join(self.folder_data, filename)
            # handle archived records
            if filter_archive:
                df = self.data.query("RecStatus == 'On'")
            else:
                df = self.data.copy()
            # filter default columns:
            df = df[self._get_organized_columns()]
            df.to_csv(filepath, sep=self.file_data_sep, index=False)
            return filepath
        else:
            return 1

    def set(self, dict_setter, load_data=True):
        """Set selected attributes based on an incoming dictionary.
        Expected to increment superior methods.

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict

        :param load_data: option for loading data from incoming file. Default is True.
        :type load_data: bool

        """
        # ignore color
        dict_setter[self.color_field] = None
        super().set(dict_setter=dict_setter, load_data=False)

        # ---------- set basic attributes --------- #

        # -------------- set data logic here -------------- #
        if load_data:
            self.load_data(file_data=self.file_data)
            self.refresh_data()

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

    def refresh_data(self):
        """Refresh data method for the object operator.
        Performs spreadsheet-like formulas for columns.

        :return: None
        :rtype: None
        """
        if self.operator is not None:
            for c in self.operator:
                self.data[c] = self.operator[c]()
        # update object
        self.update()

    def load_data(self, file_data):
        """Load data from file.
        Expected to overwrite superior methods.

        :param file_data: file path to data.
        :type file_data: str
        :return: None
        :rtype: None
        """
        # -------------- overwrite relative path input -------------- #
        self.file_data = os.path.abspath(file_data)
        # -------------- implement loading logic -------------- #

        # -------------- call loading function -------------- #
        df = pd.read_csv(self.file_data, sep=self.file_data_sep)

        # -------------- post-loading logic -------------- #
        self.set_data(input_df=df)

        return None

    def set_data(self, input_df, append=True, inplace=True):
        """Set RecordTable data from incoming dataframe.
        It handles if the dataframe has or not the required RT columns
        Base Method. Expected to be incremented downstream.

        :param input_df: incoming dataframe
        :type input_df: dataframe

        :param append: option for appending the dataframe to existing data. Default True
        :type append: bool

        :param inplace: option for overwrite data. Else return dataframe. Default True
        :type inplace: bool

        :return: None
        :rtype: None
        """
        list_input_cols = list(input_df.columns)

        # overwrite RecTable column
        input_df[self.rectable_field] = self.name

        # handle RecId
        if self.recid_field not in list_input_cols:
            # enforce Id based on index
            n_last_id = self._last_id_int()
            n_incr = n_last_id + 1
            input_df[self.recid_field] = [
                "Rec" + str(_ + n_incr).zfill(self.id_size) for _ in input_df.index
            ]
        else:
            # remove incoming duplicates
            input_df.drop_duplicates(subset=self.recid_field, inplace=True)

        # handle timestamp
        if self.rectimest_field not in list_input_cols:
            input_df[self.rectimest_field] = self._get_timestamp()

        # handle timestamp
        if self.recstatus_field not in list_input_cols:
            input_df[self.recstatus_field] = "On"

        # Add missing columns with default values
        for column in self._get_organized_columns():
            if column not in input_df.columns:
                input_df[column] = ""
        df_merged = input_df[self._get_organized_columns()]

        # concatenate dataframes
        if append:
            if self.data is not None:
                df_merged = pd.concat([self.data, df_merged], ignore_index=True)

        if inplace:
            # pass copy
            self.data = df_merged.copy()
            return None
        else:
            return df_merged

    def insert_record(self, dict_rec):
        """Insert a record in the RT

        :param dict_rec: input record dictionary
        :type dict_rec: dict
        :return: None
        :rtype: None
        """

        # ------ parse expected fields ------- #
        # filter expected columns
        dict_rec_filter = self._filter_dict_rec(input_dict=dict_rec)
        # ------ set default fields ------- #
        # set table field
        dict_rec_filter[self.rectable_field] = self.name
        # create index
        dict_rec_filter[self.recid_field] = self._next_recid()
        # compute timestamp
        dict_rec_filter[self.rectimest_field] = self._get_timestamp()
        # set active
        dict_rec_filter[self.recstatus_field] = "On"

        # ------ merge ------- #
        # create single-row dataframe
        df = pd.DataFrame({k: [dict_rec_filter[k]] for k in dict_rec_filter})
        # concat to data
        self.data = pd.concat([self.data, df]).reset_index(drop=True)

        self.update()
        return None

    def edit_record(self, rec_id, dict_rec, filter_dict=True):
        """Edit RT record

        :param rec_id: record id
        :type rec_id: str
        :param dict_rec: incoming record dictionary
        :type dict_rec: dict
        :param filter_dict: option for filtering incoming record
        :type filter_dict: bool
        :return: None
        :rtype: None
        """
        # input dict rec data
        if filter_dict:
            dict_rec_filter = self._filter_dict_rec(input_dict=dict_rec)
        else:
            dict_rec_filter = dict_rec
        # include timestamp for edit operation
        dict_rec_filter[self.rectimest_field] = self._get_timestamp()

        # get data
        df = self.data.copy()
        # set index
        df = df.set_index(self.recid_field)
        # get filter series by rec id
        sr = df.loc[rec_id].copy()

        # update edits
        for k in dict_rec_filter:
            sr[k] = dict_rec_filter[k]

        # set in row
        df.loc[rec_id] = sr
        # restore index
        df.reset_index(inplace=True)
        self.data = df.copy()

        return None

    def archive_record(self, rec_id):
        """Archive a record in the RT, that is ``RecStatus`` = ``Off``

        :param rec_id: record id
        :type rec_id: str
        :return: None
        :rtype: None
        """
        dict_rec = {self.recstatus_field: "Off"}
        self.edit_record(rec_id=rec_id, dict_rec=dict_rec, filter_dict=False)
        return None

    def get_record(self, rec_id):
        """Get a record dict by id

        :param rec_id: record id
        :type rec_id: str
        :return: record dictionary
        :rtype: dict
        """
        # set index
        df = self.data.set_index(self.recid_field)

        # locate series by index and convert to dict
        dict_rec = {self.recid_field: rec_id}
        dict_rec.update(dict(df.loc[rec_id].copy()))
        return dict_rec

    def get_record_df(self, rec_id):
        """Get a record dataframe by id

        :param rec_id: record id
        :type rec_id: str
        :return: record dictionary
        :rtype: dict
        """
        # get dict
        dict_rec = self.get_record(rec_id=rec_id)
        # convert in vertical dataframe
        dict_df = {
            "Field": [k for k in dict_rec],
            "Value": [dict_rec[k] for k in dict_rec],
        }
        return pd.DataFrame(dict_df)

    def load_record_data(
        self, file_record_data, input_field="Field", input_value="Value"
    ):
        """Load record data from a ``csv`` file to a dict

        .. note::

            This method **does not insert** the record data to the ``RecordTable``.


        :param file_record_data: file path to ``csv`` file.
        :type file_record_data: str
        :param input_field: Name of ``Field`` column in the file.
        :type input_field:
        :param input_value: Name of ``Value`` column in the file.
        :type input_value:
        :return: record dictionary
        :rtype: dict
        """
        # load record from file
        df = pd.read_csv(
            file_record_data, sep=self.file_data_sep, usecols=[input_field, input_value]
        )
        # convert into a dict
        dict_rec_raw = {
            df[input_field].values[i]: df[input_value].values[i] for i in range(len(df))
        }

        # filter for expected data columns
        dict_rec = {}
        for c in self.columns_data:
            if c in dict_rec_raw:
                dict_rec[c] = dict_rec_raw[c]

        return dict_rec

    def export_record(self, rec_id, filename=None, folder_export=None):
        """Export a record from the table to a ``csv`` file.

        :param rec_id: record id
        :type rec_id: str
        :param filename: file name (name alone, without file extension)
        :type filename: str
        :param folder_export: folder to export
        :type folder_export: str
        :return: path to exported file
        :rtype: str
        """
        # retrieve dataframe
        df = self.get_record_df(rec_id=rec_id)
        # handle filename and folder
        if filename is None:
            filename = self.name + "_" + rec_id
        if folder_export is None:
            folder_export = self.folder_data
        filepath = os.path.join(folder_export, filename + ".csv")
        # save
        df.to_csv(filepath, sep=self.file_data_sep, index=False)
        return filepath

    # ----------------- STATIC METHODS ----------------- #
    @staticmethod
    def timedelta_disagg(timedelta):
        """Util static method for dissaggregation of time delta

        :param timedelta: TimeDelta object from pandas
        :type timedelta: :class:`pandas.TimeDelta`
        :return: dictionary of time delta
        :rtype: dict
        """
        days = timedelta.days
        years, days = divmod(days, 365)
        months, days = divmod(days, 30)
        hours, remainder = divmod(timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {
            "Years": years,
            "Months": months,
            "Days": days,
            "Hours": hours,
            "Minutes": minutes,
            "Seconds": seconds,
        }

    @staticmethod
    def timedelta_to_str(timedelta, dct_struct):
        """Util static method for string conversion of timedelta

        :param timedelta: TimeDelta object from pandas
        :type timedelta: :class:`pandas.TimeDelta`
        :param dct_struct: Dictionary of string strucuture. Ex: {'Expected days': 'Days'}
        :type dct_struct: dict
        :return: text of time delta
        :rtype: str
        """
        dct_td = RecordTable.timedelta_disagg(timedelta=timedelta)
        parts = []
        for k in dct_struct:
            parts.append("{}: {}".format(dct_struct[k], dct_td[k]))
        return ", ".join(parts)

    @staticmethod
    def running_time(start_datetimes, kind="raw"):
        """Util static method for computing the runnning time for a list of starting dates

        :param start_datetimes: List of starting dates
        :type start_datetimes: list
        :param kind: mode for output format ('raw', 'human' or 'age')
        :type kind: str
        :return: list of running time
        :rtype: list
        """
        # Convert 'start_datetimes' to datetime format
        start_datetimes = pd.to_datetime(start_datetimes)
        # Calculate the running time as a timedelta
        current_datetime = pd.to_datetime("now")
        running_time = current_datetime - start_datetimes
        # Apply the custom function to create a new column
        if kind == "raw":
            running_time = running_time.tolist()
        elif kind == "human":
            dct_str = {"Years": "yr", "Months": "mth"}
            running_time = running_time.apply(
                RecordTable.timedelta_to_str, args=(dct_str,)
            )
        elif kind == "age":
            running_time = [int(e.days / 365) for e in running_time]

        return running_time
