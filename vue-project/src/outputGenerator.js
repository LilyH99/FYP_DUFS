// Generates a ZIP file with the proper folder structure 

import JSZip from 'jszip'
import { saveAs } from 'file-saver'

/**
 * Generate and download a ZIP file containing the unit file structure
 * @param {Object} unitFiles - Object containing files for each section
 * @param {Array} sections - Array of section definitions
 * @param {String} unitCode - Unit code (e.g., "COS12345")
 * @param {String} unitName - Unit name (e.g., "Computing Technology Project A")
 */
export async function generateUnitFileOutput(unitFiles, sections, unitCode = 'COS12345', unitName = 'Course Name') {
  const zip = new JSZip()
  
  // Create root folder
  const rootFolderName = `${unitCode} ${unitName} Digital Unit File`
  const rootFolder = zip.folder(rootFolderName)
  
  // Create unit code subfolder
  const unitFolder = rootFolder.folder(`${unitCode} ${unitName}`)
  
  // Add files to each section folder
  for (const section of sections) {
    const sectionFiles = unitFiles[section.id] || []
    
    // Create the section folder
    const sectionFolder = unitFolder.folder(section.title)
    
    // Add files to this section
    if (sectionFiles.length > 0) {
      for (const file of sectionFiles) {
        try {
          // Read the file as binary data
          const fileData = await readFileAsArrayBuffer(file)
          sectionFolder.file(file.name, fileData)
        } catch (error) {
          console.error(`Error adding file ${file.name}:`, error)
        }
      }
    } else {
      // If folder is empty, add a placeholder .gitkeep file
      // (some sections like 8.0 and 9.0 might be empty)
      sectionFolder.file('.gitkeep', '')
    }
  }
  
  // Generate the ZIP file
  try {
    const blob = await zip.generateAsync({ 
      type: 'blob',
      compression: 'DEFLATE',
      compressionOptions: {
        level: 6
      }
    })
    
    // Trigger download
    const timestamp = new Date().toISOString().split('T')[0]
    const filename = `${unitCode}_Digital_Unit_File_${timestamp}.zip`
    saveAs(blob, filename)
    
    return { success: true, message: 'Unit file generated successfully!' }
  } catch (error) {
    console.error('Error generating ZIP:', error)
    return { success: false, message: 'Failed to generate unit file.' }
  }
}

/**
 * Helper function to read a file as ArrayBuffer
 * @param {File} file - The file to read
 * @returns {Promise<ArrayBuffer>}
 */
function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = (e) => reject(e)
    reader.readAsArrayBuffer(file)
  })
}

/**
 * Preview the folder structure that will be generated
 * @param {Object} unitFiles - Object containing files for each section
 * @param {Array} sections - Array of section definitions
 * @returns {Object} Structure summary
 */
export function previewStructure(unitFiles, sections) {
  const structure = {}
  let totalFiles = 0
  
  for (const section of sections) {
    const files = unitFiles[section.id] || []
    structure[section.title] = {
      fileCount: files.length,
      files: files.map(f => f.name)
    }
    totalFiles += files.length
  }
  
  return {
    totalFiles,
    totalFolders: sections.length,
    structure
  }
}