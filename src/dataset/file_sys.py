from .base import DataSet


class FileSys(DataSet):
    """
    The core ``FileSys`` base/demo object. File System object.
    Useful for complex folder structure setups and controlling the status_t1
    of expected file.
    This is a Base and Dummy object. Expected to be implemented downstream for
    custom applications.

    """

    def __init__(self, folder_base, name="MyFS", alias="FS0"):
        """Initialize the ``FileSys`` object.
        Expected to increment superior methods.

        :param folder_base: path to File System folder location
        :type folder_base: str

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from name
        :type alias: str

        """
        # prior attributes
        self.folder_base = folder_base

        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)

        # overwriters
        self.object_alias = "FS"

        # ------------ set mutables ----------- #
        self.folder_main = os.path.join(self.folder_base, self.name)
        self._set_view_specs()

        # ... continues in downstream objects ... #

    def _set_fields(self):
        """
        Set fields names. Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()

        # Attribute fields
        self.folder_base_field = "Folder_Base"

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
            # todo include more view specs
        }
        return None

    #
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
        dict_meta_local = {self.folder_base_field: self.folder_base}

        # update
        dict_meta.update(dict_meta_local)

        # removals

        # remove color
        dict_meta.pop(self.color_field)
        # remove source
        dict_meta.pop(self.source_data_field)

        return dict_meta

    def get_structure(self):
        """Get FileSys structure dictionary. Expected to overwrite superior methods

        :return: structure dictionary
        :rtype: dict
        """
        # get pandas DataFrame
        df = self.data.copy()

        # Initialize the nested dictionary
        dict_structure = {}

        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            current_dict = dict_structure

            # Split the folder path into individual folder names
            folders = row["Folder"].split("/")

            # Iterate over the folders to create the nested structure
            for folder in folders:
                current_dict = current_dict.setdefault(folder, {})

            # If a file is present, add it to the nested structure
            if pd.notna(row["File"]):
                current_dict[row["File"]] = [
                    row["Format"],
                    row["File_Source"] if pd.notna(row["File_Source"]) else "",
                    row["Folder_Source"] if pd.notna(row["Folder_Source"]) else "",
                ]
        return dict_structure

    def get_status(self, folder_name):  # todo dosctring
        dict_status = {}
        # get full folder path
        folder = self.folder_main + "/" + folder_name
        # filter expected files
        df = self.data.copy()
        df = df.query("Folder == '{}'".format(folder_name))
        df = df.dropna(subset=["File"])
        if len(df) == 0:
            return None
        else:
            dict_status["Folder"] = df.copy()
            dict_status["Files"] = {}
            dict_files = {}
            for i in range(len(df)):
                # get file name
                lcl_file_name = df["File"].values[i]
                dict_files[lcl_file_name] = {}
                # get file format
                lcl_file_format = df["Format"].values[i]
                # get extensions:
                dict_extensions = self.get_extensions()
                #
                list_lcl_extensions = dict_extensions[lcl_file_format]
                # print(list_lcl_extensions)
                for ext in list_lcl_extensions:
                    lcl_path = os.path.join(folder, lcl_file_name + "." + ext)
                    list_files = glob.glob(lcl_path)
                    lst_filenames_found = [os.path.basename(f) for f in list_files]
                    dict_files[lcl_file_name][ext] = lst_filenames_found
            for k in dict_files:
                # Convert each list in the dictionary to a pandas Series and then create a DataFrame
                _df = pd.DataFrame(
                    {key: pd.Series(value) for key, value in dict_files[k].items()}
                )
                if len(_df) == 0:
                    for c in _df.columns:
                        _df[c] = [None]
                _df = _df.fillna("missing")
                dict_status["Files"][k] = _df.copy()

            return dict_status

    def update(self):
        super().update()
        # set main folder
        self.folder_main = os.path.join(self.folder_base, self.name)
        # ... continues in downstream objects ... #

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

        # -------------- super -------------- #
        super().set(dict_setter=dict_setter, load_data=False)

        # ---------- set basic attributes --------- #
        # set base folder
        self.folder_base = dict_setter[self.folder_base_field]

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
        file_data = os.path.abspath(file_data)

        # -------------- implement loading logic -------------- #

        # -------------- call loading function -------------- #
        self.data = pd.read_csv(file_data, sep=self.file_data_sep)

        # -------------- post-loading logic -------------- #

        return None

    def setup(self):
        """
        This method sets up all the FileSys structure (default folders and files)

        .. danger::

            This method overwrites all existing default files.

        """
        # update structure
        self.structure = self.get_structure()

        # make main dir
        self.make_dir(str_path=self.folder_main)

        # fill structure
        FileSys.fill(dict_struct=self.structure, folder=self.folder_main)

    def backup(
        self,
        location_dir,
        version_id="v-0-0",
    ):  # todo docstring
        dst_dir = os.path.join(location_dir, self.name + "_" + version_id)
        FileSys.archive_folder(src_dir=self.folder_main, dst_dir=dst_dir)
        return None

    def view(self, show=True):  # todo implement
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

        # fig = plt.figure(figsize=(specs["width"], specs["height"]))  # Width, Height

        # --------------------- plotting --------------------- #

        # --------------------- post-plotting --------------------- #
        # set basic plotting stuff

        # Adjust layout to prevent cutoff
        # plt.tight_layout()

        # --------------------- end --------------------- #
        # show or save
        if show:
            # plt.show()
            return None
        else:
            file_path = "{}/{}.{}".format(
                specs["folder"], specs["filename"], specs["fig_format"]
            )
            plt.savefig(file_path, dpi=specs["dpi"])
            plt.close(fig)
            return file_path

    # ----------------- STATIC METHODS ----------------- #
    @staticmethod
    def archive_folder(src_dir, dst_dir):
        """archive to a zip folder

        :param src_dir: source directory
        :type src_dir: str
        :param dst_dir: destination directory
        :type dst_dir: str
        :return: None
        :rtype: None
        """
        # Create a zip archive from the directory
        shutil.make_archive(dst_dir, "zip", src_dir)
        return None

    @staticmethod
    def merge_pdfs(lst_pdfs, dst_dir, output_filename):
        """Merge PDF files to a single PDF

        :param lst_pdfs: list of PDFs file paths
        :type lst_pdfs: list
        :param dst_dir: path to destination folder
        :type dst_dir: str
        :param output_filename: name of output file (without extension)
        :type output_filename: str
        :return: path to output file
        :rtype: str
        """
        if len(lst_pdfs) == 0:
            return None
        else:
            output_pdf = f"{dst_dir}/{output_filename}.pdf"
            pdf_writer = PyPDF2.PdfWriter()
            for pdf in lst_pdfs:
                with open(pdf, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)

            with open(output_pdf, "wb") as output_file:
                pdf_writer.write(output_file)

            return output_pdf

    @staticmethod
    def get_extensions():
        list_basics = [
            "pdf",
            "docx",
            "xlsx",
            "bib",
            "tex",
            "svg",
            "png",
            "jpg",
            "txt",
            "csv",
            "qml",
            "tif",
            "gpkg",
        ]
        dict_extensions = {e: [e] for e in list_basics}
        dict_aliases = {
            "table": ["csv"],
            "raster": ["asc", "prj", "qml"],
            "qraster": ["asc", "prj", "csv", "qml"],
            "fig": ["jpg"],
            "vfig": ["svg"],
            "receipt": ["pdf", "jpg"],
        }
        dict_extensions.update(dict_aliases)
        return dict_extensions

    @staticmethod
    def check_file_status(files):
        """Static method for file existing checkup

        :param files: iterable with file paths
        :type files: list
        :return: list status_t1 ('ok' or 'missing')
        :rtype: list
        """
        list_status = []
        for f in files:
            str_status = "missing"
            if os.path.isfile(f):
                str_status = "ok"
            list_status.append(str_status)
        return list_status

    @staticmethod
    def make_dir(str_path):
        """Util function for making a diretory

        :param str_path: path to dir
        :type str_path: str
        :return: None
        :rtype: None
        """
        if os.path.isdir(str_path):
            pass
        else:
            os.mkdir(str_path)
        return None

    @staticmethod
    def copy_batch(dst_pattern, src_pattern):
        """Util static method for batch-copying pattern-based files.

        .. note::

            Pattern is expected to be a prefix prior to ``*`` suffix.

        :param dst_pattern: destination path with file pattern. Example: path/to/dst_file_*.csv
        :type dst_pattern: str
        :param src_pattern: source path with file pattern. Example: path/to/src_file_*.csv
        :type src_pattern: str
        :return: None
        :rtype: None
        """
        # handle destination variables
        dst_basename = os.path.basename(dst_pattern).split(".")[0].replace("*", "")  # k
        dst_folder = os.path.dirname(dst_pattern)  # folder

        # handle sourced variables
        src_extension = os.path.basename(src_pattern).split(".")[1]
        src_prefix = os.path.basename(src_pattern).split(".")[0].replace("*", "")

        # get the list of sourced files
        list_files = glob.glob(src_pattern)
        # copy loop
        if len(list_files) != 0:
            for _f in list_files:
                _full = os.path.basename(_f).split(".")[0]
                _suffix = _full[len(src_prefix) :]
                _dst = os.path.join(
                    dst_folder, dst_basename + _suffix + "." + src_extension
                )
                shutil.copy(_f, _dst)
        return None

    @staticmethod
    def fill(dict_struct, folder, handle_files=True):
        """Recursive function for filling the ``FileSys`` structure

        :param dict_struct: dicitonary of directory structure
        :type dict_struct: dict

        :param folder: path to local folder
        :type folder: str

        :return: None
        :rtype: None
        """

        def handle_file(dst_name, lst_specs, dst_folder):
            """Sub routine for handling expected files in the FileSys structure.

            :param dst_name: destination filename
            :type dst_name: str
            :param lst_specs: list for expected file specifications
            :type lst_specs: list
            :param dst_folder: destination folder
            :type dst_folder: str
            :return: None
            :rtype: None
            """
            dict_exts = FileSys.get_extensions()
            lst_exts = dict_exts[lst_specs[0]]
            src_name = lst_specs[1]
            src_dir = lst_specs[2]

            # there is a sourcing directory
            if os.path.isdir(src_dir):
                # extension loop:
                for extension in lst_exts:
                    # source
                    src_file = src_name + "." + extension
                    src_filepath = os.path.join(src_dir, src_file)
                    # destination
                    dst_file = dst_name + "." + extension
                    dst_filepath = os.path.join(dst_folder, dst_file)
                    #
                    # there might be a sourced file
                    if os.path.isfile(src_filepath):
                        shutil.copy(src=src_filepath, dst=dst_filepath)
                    elif "*" in src_name:
                        # is a pattern file
                        FileSys.copy_batch(
                            src_pattern=src_filepath, dst_pattern=dst_filepath
                        )
                    else:
                        pass

            return None

        # structure loop:
        for k in dict_struct:
            # get current folder or file
            _d = folder + "/" + k

            # [case 1] bottom is a folder
            if isinstance(dict_struct[k], dict):
                # make a dir
                FileSys.make_dir(str_path=_d)
                # now move down:
                FileSys.fill(dict_struct=dict_struct[k], folder=_d)

            # bottom is an expected file
            else:
                if handle_files:
                    handle_file(dst_name=k, lst_specs=dict_struct[k], dst_folder=folder)

        return None
