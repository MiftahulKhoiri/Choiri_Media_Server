#!/usr/bin/env python3
"""
Script untuk update Git dari repository khusus
URL Repository: https://github.com/MiftahulKhoiri/Choiri_Media_Server.git
"""

import os
import sys
import shutil
import subprocess
import tempfile
import requests
import tarfile
import zipfile
from pathlib import Path

class GitUpdater:
    def __init__(self, repo_url=None):
        self.repo_url = repo_url or "https://github.com/MiftahulKhoiri/Choiri_Media_Server.git"
        self.temp_dir = tempfile.mkdtemp(prefix="git_update_")
        self.current_version = self.get_current_git_version()
        
    def get_current_git_version(self):
        """Mendapatkan versi Git saat ini"""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            version_line = result.stdout.strip()
            version = version_line.split()[-1]
            print(f"Versi Git saat ini: {version}")
            return version
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Git tidak terinstall atau tidak ditemukan")
            return None
    
    def install_dependencies(self):
        """Menginstall dependencies yang diperlukan"""
        print("Menginstall dependencies untuk kompilasi Git...")
        
        distro = self.get_linux_distro()
        
        if distro in ['ubuntu', 'debian']:
            cmd = [
                'apt-get', 'update',
                '&&', 'apt-get', 'install', '-y',
                'build-essential', 'libssl-dev', 'libcurl4-gnutls-dev',
                'libexpat1-dev', 'gettext', 'zlib1g-dev', 'autoconf',
                'libz-dev', 'dh-autoreconf'
            ]
        elif distro in ['centos', 'fedora', 'rhel']:
            cmd = [
                'yum', 'groupinstall', '-y', 'Development Tools',
                '&&', 'yum', 'install', '-y',
                'openssl-devel', 'curl-devel', 'expat-devel',
                'gettext-devel', 'zlib-devel', 'perl-ExtUtils-MakeMaker'
            ]
        else:
            print(f"Distribusi {distro} tidak dikenali. Menggunakan perintah Ubuntu/Debian.")
            cmd = [
                'apt-get', 'update',
                '&&', 'apt-get', 'install', '-y',
                'build-essential', 'libssl-dev', 'libcurl4-gnutls-dev',
                'libexpat1-dev', 'gettext', 'zlib1g-dev', 'autoconf'
            ]
        
        try:
            subprocess.run(' '.join(cmd), shell=True, check=True)
            print("Dependencies berhasil diinstall")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Gagal menginstall dependencies: {e}")
            return False
    
    def get_linux_distro(self):
        """Mendeteksi distribusi Linux"""
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content:
                    return 'ubuntu'
                elif 'centos' in content or 'rhel' in content:
                    return 'centos'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'arch' in content:
                    return 'arch'
                else:
                    return 'unknown'
        except:
            return 'unknown'
    
    def clone_and_compile_git(self):
        """Clone dan compile Git dari repository"""
        print(f"Mengclone repository dari: {self.repo_url}")
        
        repo_dir = os.path.join(self.temp_dir, "git_source")
        
        try:
            # Clone repository
            if os.path.exists(repo_dir):
                print("Directory sudah ada, melakukan update...")
                subprocess.run(['git', '-C', repo_dir, 'pull'], check=True)
            else:
                subprocess.run(['git', 'clone', self.repo_url, repo_dir], check=True)
            
            os.chdir(repo_dir)
            
            # Cek apakah ini repository Git source
            if not os.path.exists('configure.ac') and not os.path.exists('Makefile'):
                print("Repository tidak berisi source code Git yang valid")
                
                # Coba cari directory yang berisi source
                for root, dirs, files in os.walk(repo_dir):
                    if 'configure.ac' in files or 'Makefile' in files:
                        os.chdir(root)
                        print(f"Menemukan source di: {root}")
                        break
                else:
                    print("Tidak ditemukan source code Git dalam repository")
                    return False
            
            # Compile Git
            print("Mengkompilasi Git...")
            
            compile_steps = [
                ['make', 'configure'],
                ['./configure', '--prefix=/usr/local'],
                ['make', 'all', '-j', str(os.cpu_count())],
                ['sudo', 'make', 'install']
            ]
            
            for step in compile_steps:
                print(f"Menjalankan: {' '.join(step)}")
                subprocess.run(step, check=True)
            
            # Verifikasi
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            new_version = result.stdout.strip()
            print(f"Git berhasil diupdate: {new_version}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error saat mengkompilasi Git: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def cleanup(self):
        """Membersihkan file temporary"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"Directory temporary dihapus: {self.temp_dir}")
    
    def run(self):
        """Menjalankan proses update"""
        print("=" * 50)
        print("UPDATE GIT DARI REPOSITORY KHUSUS")
        print("=" * 50)
        
        if not self.install_dependencies():
            print("Gagal menginstall dependencies")
            return False
        
        if not self.clone_and_compile_git():
            print("Gagal mengupdate Git")
            self.cleanup()
            return False
        
        self.cleanup()
        print("Proses update selesai!")
        return True

def main():
    # URL repository khusus
    custom_repo_url = "https://github.com/MiftahulKhoiri/Choiri_Media_Server.git"
    
    # Buat instance dan jalankan updater
    updater = GitUpdater(custom_repo_url)
    
    # Jalankan update
    success = updater.run()
    
    if success:
        print("✅ Git berhasil diupdate!")
        sys.exit(0)
    else:
        print("❌ Gagal mengupdate Git")
        sys.exit(1)

if __name__ == "__main__":
    # Cek apakah dijalankan sebagai root/sudo
    if os.geteuid() != 0:
        print("Script perlu dijalankan dengan hak akses root (sudo)")
        print("Gunakan: sudo python3 update_git.py")
        sys.exit(1)
    
    main()