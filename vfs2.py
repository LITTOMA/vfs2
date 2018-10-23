import struct


class VFS2(object):

    class Folder(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.parent, self.unk3, 
            self.file_id_start) = struct.unpack('iiiii', fs.read(struct.calcsize('iiiii')))
            self.entries = []
            self.name = ''

    class File(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.compress_type, self.parent, 
            self.data_offset, self.data_size) = struct.unpack('iiiiii', fs.read(struct.calcsize('iiiiii')))
            self.name = ''
        
    def __init__(self, fp=None):
        if fp:
            self.load_vfs2(fp)
        else:
            #Create a vfs2 object if no file input. (Default)
            self.create_vfs2()

    #Pass a 'file' object as 'fp' here is recommended.
    def load_vfs2(self, fp):
        if isinstance(fp, str):
            fp = open(fp, 'rb')
        if not isinstance(fp, file):
            raise TypeError('No file input.')
        
        sig = fp.read(4)
        if sig != 'VFS2':
            raise TypeError("Signature error. Except: VFS2, actual: %s"%sig)

        folder_count ,= struct.unpack('i', fp.read(4))
        folders = []
        for i in range(folder_count):
            folders.append(VFS2.Folder(fp))

        file_count ,= struct.unpack('i', fp.read(4))
        files = []
        for i in range(file_count):
            files.append(VFS2.File(fp))
        
        self.name_table_offset ,= struct.unpack('i', fp.read(4))
        self.data_offset = fp.tell()

        fp.seek(self.name_table_offset, 0)
        filename_count ,= struct.unpack('i', fp.read(4))
        for i in range(filename_count):
            str_len ,= struct.unpack('i', fp.read(4))
            files[i].name = fp.read(str_len)
        
        foldername_count ,= struct.unpack('i', fp.read(4))
        for i in range(foldername_count):
            str_len ,= struct.unpack('i', fp.read(4))
            folders[i].name = fp.read(str_len)
        
        for i in range(file_count):
            folder = folders[files[i].parent]
            if folder.id != files[i].parent:
                raise ValueError("Folder ID mismatch.")
            folder.entries.append(files[i])
        
        for i in range(folder_count):
            if folders[i].parent >= 0:
                folders[folders[i].parent].entries.append(folders[i])
            elif folders[i].parent == -1:
                self.tree_root = folders[i]

        fp.seek(self.data_offset, 0)
        self.fs = fp
        self.cur_node = self.tree_root

    def create_vfs2(self):
        pass
    
    def add_file(self, folder, file_path):
        pass
    
    def create_folder(self, folder, name):
        pass
    
    def exists(self, path):
        pass
    
    def extract(self, out_dir):
        pass
    
    def list(self):
        pass

    def save(self, path):
        pass


if '__main__' == __name__:
    vfs = VFS2('data.vfs')
    print vfs