import struct


class VFS2(object):

    class Folder(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.parent_id, self.unk3, 
            self.file_id_start) = struct.unpack('iiiii', fs.read(struct.calcsize('iiiii')))
            self.entries = []
            self.parent = None
            self.name = ''

    class File(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.compress_type, self.parent_id, 
            self.data_offset, self.data_size) = struct.unpack('iiiiii', fs.read(struct.calcsize('iiiiii')))
            self.parent = None
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
            folder = folders[files[i].parent_id]
            if folder.id != files[i].parent_id:
                raise ValueError("Folder ID mismatch.")
            folder.entries.append(files[i])
            files[i].parent = folder
        
        for i in range(folder_count):
            if folders[i].parent_id >= 0:
                parent = folders[folders[i].parent_id]
                parent.entries.append(folders[i])
                folders[i].parent = parent
            elif folders[i].parent_id == -1:
                self.tree_root = folders[i]
                folders[i].parent = None

        fp.seek(self.data_offset, 0)
        self.fs = fp
        self.cur_node = self.tree_root
        self.cur_depth = 0

    def create_vfs2(self):
        raise NotImplementedError("Function not supported.")
    
    def add_file(self, folder, file_path):
        raise NotImplementedError("Function not supported.")
    
    def create_folder(self, folder, name):
        raise NotImplementedError("Function not supported.")

    #cd
    def change_directory(self, path):
        if not path:
            return
        
        next_node, next_path = path.split('/', 1)
        if (not next_node) or (next_node == '.'):
            return
        
        if next_node == '..' and self.cur_node.parent_id != -1:
            self.cur_node = self.cur_node.parent
        
        for e in self.cur_node.entries:
            if e.name == next_node:
                self.cur_node = e
                break
        
        return self.change_directory(next_path)
    
    def exists(self, path):
        pass
    
    def extract(self, out_dir):
        pass
    
    def list_dir(self):
        for e in self.cur_node.entries:
            print e.name

    def save(self, path):
        pass


if '__main__' == __name__:
    vfs = VFS2('data.vfs')
    vfs.change_directory('fonts/')
    vfs.list_dir()
