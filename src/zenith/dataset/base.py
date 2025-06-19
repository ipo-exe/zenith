from ..base import MbaE


class DataSet(MbaE):
    """
    The core ``DataSet`` base/demo object.
    Expected to hold one :class:`pandas.DataFrame`.
    This is a Base and Dummy object. Expected to be implemented downstream for
    custom applications.

    **Examples**

    Here's how to use the ``DataSet`` class:

    Import Dataset

    .. code-block:: python

        # import Dataset
        from plans.src_root import DataSet

    Instantiate DataSet Object

    .. code-block:: python

        # instantiate DataSet object
        ds = DataSet(name="DataSet_1", alias="DS1")

    Set Object and Load Data

    .. code-block:: python

        # set object and load data.
        # Note: this dummy object expects "RM", "P", and "TempDB" as columns in data
        ds.set(
            dict_setter={
                "Name": "DataSet_2",
                "Alias": "DS2",
                "Color": "red",
                "Source": "",
                "Description": "This is DataSet Object",
                "File_Data": "/content/data_ds1.csv"
            },
            load_data=True
        )

    Check Data

    .. code-block:: python

        # check data `pandas.DataFrame`
        print(ds.data.head())

    Reload New Data from File

    .. code-block:: python

        # re-load new data from file
        ds.load_data(file_data="/content/data_ds2.csv")

    Get Basic Visual

    .. code-block:: python

        # get basic visual
        ds.view(show=True)

    Customize View Parameters

    .. code-block:: python

        # customize view parameters via the view_specs attribute:
        ds.view_specs["title"] = "My Custom Title"
        ds.view_specs["xlabel"] = "The X variable"
        ds.view(show=True)

    Save the Figure

    .. code-block:: python

        # save the figure
        ds.view_specs["folder"] = "path/to/folder"
        ds.view_specs["filename"] = "my_visual"
        ds.view_specs["fig_format"] = "png"
        ds.view(show=False)


    """

    def __init__(self, name: str ="MyDataSet", alias: str="DS0"):
        """Initialize the ``DataSet`` object.
        Expected to increment superior methods.

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from name
        :type alias: str

        """
        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)
        # overwriters
        self.object_alias = "DS"

        # ------------ set mutables ----------- #
        self.file_data = None
        self.folder_data = None
        self.data = None
        self.size = None

        # descriptors
        self.source_data = None
        self.descri_data = None

        # ------------ set defaults ----------- #
        self.color = "blue"
        self.file_data_sep = ";"

        # UPDATE
        self.update()

        # ... continues in downstream objects ... #

    def __str__(self):
        """
        The ``DataSet`` string.
        Expected to overwrite superior methods.

        """
        str_super = super().__str__()
        if self.data is None:
            str_df_data = "None"
            str_out = "{}\nData:\n{}\n".format(str_super, str_df_data)
        else:
            # first 5 rows
            str_df_data_head = self.data.head().to_string(index=False)
            str_df_data_tail = self.data.tail().to_string(index=False)
            str_out = "{}\nData:\n{}\n ... \n{}\n".format(
                str_super, str_df_data_head, str_df_data_tail
            )
        return str_out

    def _set_fields(self):
        """Set fields names.
        Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()
        # Attribute fields
        self.filedata_field = "File_Data"
        self.size_field = "Size"
        self.color_field = "Color"
        self.source_data_field = "Source"
        self.descri_data_field = "Description"

        # ... continues in downstream objects ... #

    def _set_view_specs(self):
        """Set view specifications.
        Expected to overwrite superior methods.

        :return: None
        :rtype: None
        """
        self.view_specs = {
            "folder": self.folder_data,
            "filename": self.name,
            "fig_format": "jpg",
            "dpi": 300,
            "title": self.name,
            "width": 5 * 1.618,
            "height": 5 * 1.618,
            "xvar": "RM",
            "yvar": "TempDB",
            "xlabel": "RM",
            "ylabel": "TempDB",
            "color": self.color,
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
        }
        return None

    def get_metadata(self):
        """Get a dictionary with object metadata.
        Expected to increment superior methods.

        .. note::

            Metadata does **not** necessarily inclue all object attributes.

        :return: dictionary with all metadata
        :rtype: dict
        """
        # ------------ call super ----------- #
        dict_meta = super().get_metadata()

        # customize local metadata:
        dict_meta_local = {
            self.size_field: self.size,
            self.color_field: self.color,
            self.source_data_field: self.source_data,
            self.descri_data_field: self.descri_data,
            self.filedata_field: self.file_data,
        }

        # update
        dict_meta.update(dict_meta_local)
        return dict_meta

    def update(self):
        """Refresh all mutable attributes based on data (includins paths).
        Base method. Expected to be incremented downstrem.

        :return: None
        :rtype: None
        """
        # refresh all mutable attributes

        # set fields
        self._set_fields()

        if self.data is not None:
            # data size (rows)
            self.size = len(self.data)

        # update data folder
        if self.file_data is not None:
            # set folder
            self.folder_data = os.path.abspath(os.path.dirname(self.file_data))
        else:
            self.folder_data = None

        # view specs at the end
        self._set_view_specs()

        # ... continues in downstream objects ... #
        return None

    def set(self, dict_setter, load_data=True):
        """Set selected attributes based on an incoming dictionary.
        Expected to increment superior methods.

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict

        :param load_data: option for loading data from incoming file. Default is True.
        :type load_data: bool

        """
        super().set(dict_setter=dict_setter)

        # ---------- settable attributes --------- #

        # COLOR
        self.color = dict_setter[self.color_field]

        # DATA: FILE AND FOLDER
        # handle if only filename is provided
        if os.path.isfile(dict_setter[self.filedata_field]):
            file_data = dict_setter[self.filedata_field][:]
        else:
            # assumes file is in the same folder as the boot-file
            file_data = os.path.join(
                self.folder_bootfile, dict_setter[self.filedata_field][:]
            )
        self.file_data = os.path.abspath(file_data)

        # -------------- set data logic here -------------- #
        if load_data:
            self.load_data(file_data=self.file_data)

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

    def load_data(self, file_data):
        """Load data from file. Expected to overwrite superior methods.

        :param file_data: file path to data.
        :type file_data: str
        :return: None
        :rtype: None
        """

        # -------------- overwrite relative path input -------------- #
        self.file_data = os.path.abspath(file_data)

        # -------------- implement loading logic -------------- #
        default_columns = {
            #'DateTime': 'datetime64[1s]',
            "P": float,
            "RM": float,
            "TempDB": float,
        }
        # -------------- call loading function -------------- #
        self.data = pd.read_csv(
            self.file_data,
            sep=self.file_data_sep,
            dtype=default_columns,
            usecols=list(default_columns.keys()),
        )

        # -------------- post-loading logic -------------- #
        self.data.dropna(inplace=True)

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

        return None

    def view(self, show=True):
        """Get a basic visualization.
        Expected to overwrite superior methods.

        :param show: option for showing instead of saving.
        :type show: bool

        :return: None or file path to figure
        :rtype: None or str

        **Notes:**

        - Uses values in the ``view_specs()`` attribute for plotting

        **Examples:**

        Simple visualization:

        >>> ds.view(show=True)

        Customize view specs:

        >>> ds.view_specs["title"] = "My Custom Title"
        >>> ds.view_specs["xlabel"] = "The X variable"
        >>> ds.view(show=True)

        Save the figure:

        >>> ds.view_specs["folder"] = "path/to/folder"
        >>> ds.view_specs["filename"] = "my_visual"
        >>> ds.view_specs["fig_format"] = "png"
        >>> ds.view(show=False)

        """
        # get specs
        specs = self.view_specs.copy()

        # --------------------- figure setup --------------------- #
        fig = plt.figure(figsize=(specs["width"], specs["height"]))  # Width, Height

        # --------------------- plotting --------------------- #
        plt.scatter(
            self.data[specs["xvar"]],
            self.data[specs["yvar"]],
            marker=".",
            color=specs["color"],
        )

        # --------------------- post-plotting --------------------- #
        # set basic plotting stuff
        plt.title(specs["title"])
        plt.ylabel(specs["ylabel"])
        plt.xlabel(specs["xlabel"])

        # handle min max
        if specs["xmin"] is None:
            specs["xmin"] = self.data[specs["xvar"]].min()
        if specs["ymin"] is None:
            specs["ymin"] = self.data[specs["yvar"]].min()
        if specs["xmax"] is None:
            specs["xmax"] = self.data[specs["xvar"]].max()
        if specs["ymax"] is None:
            specs["ymax"] = self.data[specs["yvar"]].max()

        plt.xlim(specs["xmin"], specs["xmax"])
        plt.ylim(specs["ymin"], 1.2 * specs["ymax"])

        # Adjust layout to prevent cutoff
        plt.tight_layout()

        # --------------------- end --------------------- #
        # show or save
        if show:
            plt.show()
            return None
        else:
            file_path = "{}/{}.{}".format(
                specs["folder"], specs["filename"], specs["fig_format"]
            )
            plt.savefig(file_path, dpi=specs["dpi"])
            plt.close(fig)
            return file_path