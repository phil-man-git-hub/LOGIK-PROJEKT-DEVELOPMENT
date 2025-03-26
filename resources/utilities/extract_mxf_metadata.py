import pymxf

def extract_metadata(mxf_file_path):
    # Open the MXF file
    with pymxf.MXFFile(mxf_file_path) as mxf_file:
        metadata = {}

        # Extract the header partition
        header_partition = mxf_file.partitions[0]

        # Extract metadata items
        for item in header_partition.metadata:
            key = item.key.decode('utf-8')
            value = item.value
            metadata[key] = value

        return metadata

# Example usage
mxf_file_path = 'path/to/your/file.mxf'
metadata_dict = extract_metadata(mxf_file_path)
print(metadata_dict)
