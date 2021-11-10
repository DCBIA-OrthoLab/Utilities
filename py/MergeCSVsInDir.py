import argparse
import csv
import glob
import os
import pandas as pd
from pathlib import Path

def main(args):

    dir = args.input
    cols = args.columns
    out = args.output

    filenames = list(Path(dir).glob("*.csv"))
    filenames.sort()

    all_features = []
    db = pd.read_csv(filenames[0], low_memory=False)
    if db is not None:
        all_features = db.columns

    print(all_features)
    idx = pd.MultiIndex.from_arrays([[],[]], names=['Filename', 'Index'])
    BT = pd.DataFrame(index=idx,columns=all_features)

    for filepath in filenames:
        filename = filepath.stem
        print(filename)
        try:
            db = pd.read_csv(filepath, low_memory=False)
        except Exception as e:
            print("Failed to read the file: {}".format(filename))
            continue
        for idx, entry in db.iterrows():
            print(idx)
            print(entry)
            print(len(all_features))
            values = [entry[col] if col in db.columns else '' for col in all_features]
            print(len(values))
            BT.loc[(filename, idx), all_features] = values

    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    BT.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    color_list = ['#90CAF9','#FFC107','#40E0D0','#AF7AC5','#58D68D','#EC7063']

    col_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    for ind, col_name in enumerate(BT.columns):
        column_len = BT[col_name].astype(str).str.len().max() + 2
        if col_name in cols:
            worksheet.set_column(ind+3, ind+3, column_len, workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': color_list[cols.index(col_name)]}))

    header_format = workbook.add_format({'bold': True,'text_wrap': True,'align': 'center','valign': 'vcenter','border': 1})
    formats = []
    for col in cols:
        formats.append(workbook.add_format({'bold': True,'text_wrap': True,'align': 'center','valign': 'vcenter','border': 1, 'bg_color': color_list[cols.index(col)]}))

    BT.insert(loc=0, column='Filename', value='')
    BT.insert(loc=1, column="Index", value=0)

    # Write header
    for ind, col_name in enumerate(BT.columns.values):
        if ind < 2:
            worksheet.write(0, ind, col_name, header_format)
        else:
            if cols == ['None']:
                worksheet.write(0, ind, col_name, header_format)
            else: 
                if col_name in cols:
                    worksheet.write(0, ind, col_name, formats[cols.index(col_name)])

    for ind, ind_name in enumerate(BT.index.names):
        indexcol_len = max(BT.index.get_level_values(ind_name).astype(str).str.len().max(), len(ind_name)) + 2
        worksheet.set_column(ind, ind, indexcol_len, col_format)
    writer.save()
    print("Saved to ", out)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input','-i',default='BoneTexture/',help='input folder containing the csv bone texture files')
    parser.add_argument('--columns','-c',type=str,nargs='+',default=['None'],help='Name of the different columns for each feature')
    parser.add_argument('--output','-o',default='BoneTexture.xlsx',help='output file')
    args = parser.parse_args()

    main(args)
