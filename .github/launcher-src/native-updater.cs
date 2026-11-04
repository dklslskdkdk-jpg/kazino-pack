using System;
using System.IO;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Web.Script.Serialization;
using System.Windows.Forms;
public static class BluUpdater {
 static JavaScriptSerializer json=new JavaScriptSerializer();
 static string root,source,target,expected,version,nonce,staged,backup;
 static bool showErrors=true;
 static string Text(Dictionary<string,object> d,string k){object v;return d.TryGetValue(k,out v)?Convert.ToString(v):"";}
 static void Write(string name,object value){File.WriteAllText(Path.Combine(root,name),json.Serialize(value),new UTF8Encoding(false));}
 static void Result(string status,string message){Write("update-result.json",new {status=status,message=message,target=target,version=version,expectedHash=expected,nonce=nonce});}
 static string Hash(string file){using(var stream=File.OpenRead(file))using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(stream)).Replace("-","").ToLowerInvariant();}
 static void Remove(string file){try{if(File.Exists(file))File.Delete(file);}catch{}}
 static Process StartLauncher(){var p=new ProcessStartInfo(target);p.WorkingDirectory=Path.GetDirectoryName(target);p.UseShellExecute=false;foreach(string k in new[]{"PORTABLE_EXECUTABLE_FILE","PORTABLE_EXECUTABLE_DIR","PORTABLE_EXECUTABLE_APP_FILENAME","ELECTRON_RUN_AS_NODE","NODE_OPTIONS"})p.EnvironmentVariables.Remove(k);return Process.Start(p);}
 [STAThread] public static int Main(string[] args){
 try{
  if(args.Length!=1)throw new Exception("Falta la solicitud de actualización.");
  var data=json.Deserialize<Dictionary<string,object>>(File.ReadAllText(args[0],Encoding.UTF8));
  root=Path.GetFullPath(Text(data,"root"));source=Path.GetFullPath(Text(data,"source"));target=Path.GetFullPath(Text(data,"target"));expected=Text(data,"expectedHash").ToLowerInvariant();version=Text(data,"version");nonce=Text(data,"nonce");object flag;if(data.TryGetValue("showErrors",out flag))showErrors=Convert.ToBoolean(flag);
  if(!System.Text.RegularExpressions.Regex.IsMatch(expected,"^[a-f0-9]{64}$")||!System.Text.RegularExpressions.Regex.IsMatch(nonce,"^[a-f0-9]{32}$")||!System.Text.RegularExpressions.Regex.IsMatch(version,@"^\d{1,6}\.\d{1,6}\.\d{1,6}$")||!target.EndsWith(".exe",StringComparison.OrdinalIgnoreCase)||String.Equals(source,target,StringComparison.OrdinalIgnoreCase))throw new Exception("Solicitud de actualización inválida.");
  string allowed=Path.Combine(Path.Combine(Path.Combine(root,"updates"),version),"BluStudio-Launcher.exe");if(!String.Equals(source,allowed,StringComparison.OrdinalIgnoreCase))throw new Exception("El archivo no está en la carpeta de actualizaciones autorizada.");
  staged=target+".blu-update";backup=target+".previous";
  Write("updater-ready.json",new {nonce=nonce});
  int oldPid=Convert.ToInt32(data["pid"]);try{using(var old=Process.GetProcessById(oldPid)){if(!old.WaitForExit(45000))throw new Exception("El launcher anterior no terminó de cerrarse.");}}catch(ArgumentException){}
  if(Hash(source)!=expected)throw new Exception("La descarga no pasó la comprobación SHA-256.");
  Result("replacing","Reemplazando el launcher anterior.");bool done=false;Exception last=null;
  for(int i=0;i<90;i++){try{File.Copy(source,staged,true);if(Hash(staged)!=expected)throw new Exception("La copia temporal no pasó la verificación.");Remove(backup);File.Replace(staged,target,backup);if(Hash(target)!=expected)throw new Exception("El archivo instalado no pasó la verificación.");done=true;break;}catch(Exception error){last=error;Thread.Sleep(1000);}}
  if(!done)throw new Exception("Windows no permitió reemplazar el EXE. Se conserva el anterior. "+(last==null?"":last.Message));
  Result("starting","Abriendo y comprobando el launcher actualizado.");using(var opened=StartLauncher()){}
  bool confirmed=false;for(int i=0;i<120;i++){try{var receipt=json.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(root,"update-confirmed.json"),Encoding.UTF8));if(Text(receipt,"nonce")==nonce&&Text(receipt,"sha256").Equals(expected,StringComparison.OrdinalIgnoreCase)&&Text(receipt,"version")==version){confirmed=true;break;}}catch{}Thread.Sleep(500);}
  if(!confirmed)throw new Exception("Se reemplazó el EXE, pero no confirmó su apertura. Abre Bluu Client desde su carpeta y revisa el aviso de Windows.");
  Remove(backup);Remove(source);Remove(staged);Remove(Path.Combine(Path.GetDirectoryName(source),"actualizacion-error.txt"));Result("complete","Actualización instalada y apertura comprobada.");return 0;
 }catch(Exception error){try{if(!String.IsNullOrEmpty(root)){Result("error",error.Message);File.WriteAllText(Path.Combine(root,"updater-last-error.txt"),error.Message,Encoding.UTF8);}if(!String.IsNullOrEmpty(source))File.WriteAllText(Path.Combine(Path.GetDirectoryName(source),"actualizacion-error.txt"),error.Message,Encoding.UTF8);}catch{}if(showErrors)MessageBox.Show(error.Message,"Actualización de Bluu Client",MessageBoxButtons.OK,MessageBoxIcon.Error);return 1;
 }finally{if(!String.IsNullOrEmpty(source))Remove(source);if(!String.IsNullOrEmpty(staged))Remove(staged);if(!String.IsNullOrEmpty(root))Remove(Path.Combine(root,"updater-ready.json"));}
 }
}
