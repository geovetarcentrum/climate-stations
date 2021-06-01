% % Plot graphs and save monthly files of meteorological data from GVC roof
% station
% % is edited by Shiho Onomura (2011-12-1)
% % and Janka Konarska (2014-09-11)

clear;
try
    c=clock;
    n=floor(datenum(c));
    c=datevec(n);

% Import data, skip headers and time (first column, first 4 rows)
%tendata=dlmread('Z:\Klimatst\Nya\taket_2014b_10.dat',',',4,1); % New location 20140212.
%hourdata=dlmread('Z:\Klimatst\Nya\taket_2014b_60.dat',',',4,1); % New location 20140212
tendata=txt2mat('Z:\Klimatst\Nya\taket_2015a_10.dat',4);tendata=tendata(:,7:end);
hourdata=txt2mat('Z:\Klimatst\Nya\taket_2014b_60.dat',4);hourdata=hourdata(:,7:end);

% Copy data files from Z:\ to a local folder
copyfile('Z:\Klimatst\Nya\taket_2015a_10.dat','C:\MeteorologicalMeasurements\GVCroof\Data\taket_2015a_10.dat');
copyfile('Z:\Klimatst\Nya\taket_2014b_60.dat','C:\MeteorologicalMeasurements\GVCroof\Data\taket_2014b_60.dat');

%% Import date and time (first row)

filename = 'Z:\Klimatst\Nya\taket_2015a_10.dat'; % 10 min data
delimiter = {','};
startRow = 5;
formatSpec = '%s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'HeaderLines' ,startRow-1, ...
    'ReturnOnError', false);
fclose(fileID);
tendata_tid = [dataArray{1:end-1}];
clearvars filename delimiter startRow formatSpec fileID dataArray ans;  

% Same for hourly data
filename = 'Z:\Klimatst\Nya\taket_2014b_60.dat';
delimiter = {','};
startRow = 5;
formatSpec = '%s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%*s%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'HeaderLines' ,startRow-1, ...
    'ReturnOnError', false);
fclose(fileID);
hourdata_tid = [dataArray{1:end-1}];
clearvars filename delimiter startRow formatSpec fileID dataArray ans;  

%% Date string to serial number. Get Year, DOY, HHMM, Code
tendata_tid_sn = datenum(tendata_tid,'"yyyy-mm-dd HH:MM:SS"');
hourdata_tid_sn = datenum(hourdata_tid,'"yyyy-mm-dd HH:MM:SS"');

tendata_year = year(tendata_tid);
hourdata_year = year(hourdata_tid);

% DOY
tendata_DOY = floor(tendata_tid_sn - datenum(year(tendata_tid_sn),1,1) + 1);
hourdata_DOY = floor(hourdata_tid_sn - datenum(year(hourdata_tid_sn),1,1) + 1);

% HHMM
tendata_tid_char = char(tendata_tid);
hourdata_tid_char = char(hourdata_tid);
tendata_HH = tendata_tid_char(:,13:14); tendata_MM = tendata_tid_char(:,16:17); tendata_HM = [tendata_HH tendata_MM];
hourdata_HH = hourdata_tid_char(:,13:14); hourdata_MM = hourdata_tid_char(:,16:17); hourdata_HM = [hourdata_HH hourdata_MM];
tendata_HM = str2num(tendata_HM); hourdata_HM = str2num(hourdata_HM);
clear tendata_HH tendata_MM tendata_tid_char hourdata_HH hourdata_MM hourdata_tid_char;

% Code
tendata_code(:,1) = 110*ones(1,size(tendata,1)); 
hourdata_code(:,1) = 160*ones(1,size(hourdata,1));

%% Set the same file format as before (Code, Year, DOY, HHMM, met data)

tendata = [tendata_code tendata_year tendata_DOY tendata_HM tendata(:,2:end)]; % skip first row - record number
hourdata = [hourdata_code hourdata_year hourdata_DOY hourdata_HM hourdata(:,2:end)]; % skip first row - record number

clear hourdata_DOY hourdata_HM hourdata_code hourdata_tid hourdata_tid_sn hourdata_year ...
    tendata_DOY tendata_HM tendata_code tendata_tid tendata_tid_sn tendata_year;

%% Calculating Ldown
Ldown=tendata(:,18)+5.67051e-8.*tendata(:,17).^4;
tendata=[tendata(:,1:18) Ldown tendata(:,19:end)];
    
Ldown=hourdata(:,18)+5.67051e-8.*hourdata(:,17).^4;
hourdata=[hourdata(:,1:18) Ldown hourdata(:,19:end)];

clear Ldown

    %% Convert day of year to Julian day
    
    for k=1:size(tendata,1)
        iyear=tendata(k,2);
        doy=tendata(k,3);
        A=logical(mod(iyear,4));
        B=logical(mod(iyear,100));
        C=logical(mod(iyear,400));
        leapyear=ismember(iyear,iyear(~C | (~A & B)));
        if leapyear==1
            dayspermonth=[31 29 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>=doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        else
            dayspermonth=[31 28 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>=doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        end
        hour=floor(tendata(k,4)/100);
        min=rem(tendata(k,4)/100,1)*100;
        tendata(k,1)=datenum([iyear imonth iday hour min 0]);
    end
    
    for k=1:size(hourdata,1)
        iyear=hourdata(k,2);
        doy=hourdata(k,3);
        A=logical(mod(iyear,4));
        B=logical(mod(iyear,100));
        C=logical(mod(iyear,400));
        leapyear=ismember(iyear,iyear(~C | (~A & B)));
        if leapyear==1
            dayspermonth=[31 29 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        else
            dayspermonth=[31 28 31 30 31 30 31 31 30 31 30 31];
            i=0;
            for j=1:12
                i=i+dayspermonth(j);
                if i>doy
                    iday=doy-(i-dayspermonth(j));
                    imonth=j;
                    break;
                end
            end
        end
        hour=floor(hourdata(k,4)/100);
        hourdata(k,1)=datenum([iyear imonth iday hour 0 0]);
    end
    
    %% Saving monthly files
    y=datevec(datenum(c)-1); %%checking the date of yesterday
    lmonth=y(2);
    if lmonth~=c(2)
        if lmonth==12
            year1=c(1)-1;
        else
            year1=c(1);
        end
        if exist(['C:\MeteorologicalMeasurements\GVCroof\Data\MonthlyFiles2011_Now\gvc_roof_10mindata_'...
                num2str(year1) '_' num2str(lmonth) '.txt'],'file')==0;
            
            %day of year and check for leap year
            A=logical(mod(year1,4));
            B=logical(mod(year1,100));
            C=logical(mod(year1,400));
            leapyear=ismember(year1,year1(~C | (~A & B)));
            if leapyear==1
                dayspermonth=[31 29 31 30 31 30 31 31 30 31 30 31];
            else
                dayspermonth=[31 28 31 30 31 30 31 31 30 31 30 31];
            end
            
            if y(2)==1 % changed from c to y by Fredrik 20120402
                DOYstart=1;
                DOYend=dayspermonth(1);
            else
                DOYstart=sum(dayspermonth(1:lmonth-1))+1;
                DOYend=sum(dayspermonth(1:lmonth));
            end
            
            rowstosave= find(tendata(:,2)==year1 & tendata(:,3)>=DOYstart & tendata(:,3)<=DOYend);
            monthtendata=tendata(rowstosave,:);
            rowstosave1=find(hourdata(:,2)==year1 & hourdata(:,3)>=DOYstart & hourdata(:,3)<=DOYend);
            monthhourdata=hourdata(rowstosave1,:);
           
            
%             % Add three coloumns that is removed by new logger program 20130408
%                 badcolten=zeros(size(monthtendata,1),1)-6999;
%                 badcolhour=zeros(size(monthhourdata,1),1)-6999;           
% 
%                 if size(monthtendata,2)==19
%                 monthtendata=[monthtendata(:,1:11) badcolten badcolten monthtendata(:,12:19)];
%                 monthhourdata=[monthhourdata(:,1:11) badcolhour badcolhour monthhourdata(:,12:19)];
%             else
%                 monthtendata=[monthtendata(:,1:18) badcolten badcolten badcolten];
%                 monthhourdata=[monthhourdata(:,1:18) badcolhour badcolhour badcolten];
%             end
%             
            %Save as monthly test files
            textformat='%4s %4s %3s %4s %10s %10s %13s %9s %9s %12s %8s %8s %11s %10s %9s %8s %20s %19s %18s %10s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s %13s';
            numformat='%3d %4d %3d %4d %6.2f %6.2f %6.3f %6.3f %6.3f %6.1f %6.1f %6.2f %6.1f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.2f %6.2f %6.3f %6.3f %6.3f %6.2f %6.2f %6.1f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f';
            
            %fprintf(fn2,textformat,'Wd_min','Wd_avg','Wd_max','Ws_min','Ws_avg','Ws_max','Ta','RH','P'...
            %    ,'R_amount','R_time','R_intens','H_amount','H_time','H_intens','Ws_vec_avg','Wd_vec_avg','maxWsmean','maxWsmax','None');
            
            %write to files. New header from 8 April
            header=['Code ','Year ','DOY ','HHMM ','Ta ','RH ','Ws ','Wd ','Wd_sd ','RainPerPeriod ','CumulativeRain '...
                ,'AirPressure ','Integer ','Decimal ','GlobalRadiaion_SPN1 ','DiffuseRadiation_SPN1 ','L_tempK ','L_sig ','Ldown '...
                ,'Wd_min ','Wd_avg ','Wd_max ','Ws_min ','Ws_avg ','Ws_max ','Ta ','RH ','P '...
                ,'R_amount ','R_time ','R_intens ','H_amount ','H_time ','H_intens ','Ws_avg ','Wd_avg ','Wd_std '];
            
            % Tenminutedata
            fn2=fopen(['C:\MeteorologicalMeasurements\GVCroof\Data\MonthlyFiles2011_Now\gvc_roof_10mindata_' num2str(year1) '_' num2str(lmonth) '.txt'],'w');
            fprintf(fn2,textformat,header);
            fprintf(fn2,'\r\n');
            for p=1:length(monthtendata)
                fprintf(fn2,numformat,monthtendata(p,:));
                fprintf(fn2,'\r\n');
            end
            fclose(fn2);
            f=ftp('pc70.gvc.gu.se','urban-net');
            cd(f,'public_html');
            cd(f,'GVCdata');
            mput(f,['C:\MeteorologicalMeasurements\GVCroof\Data\MonthlyFiles2011_Now\gvc_roof_10mindata_' num2str(year1) '_' num2str(lmonth) '.txt']);
            
            
            % 60minutedata %% This is not longer active. No 60 min file is
            % create
%             fn2=fopen(['C:\MeteorologicalMeasurements\GVCroof\Data\MonthlyFiles2011_Now\gvc_roof_60mindata_' num2str(year1) '_' num2str(lmonth) '.txt'],'w');
%             fprintf(fn2,textformat,header);
%             fprintf(fn2,'\r\n');
%             for p=1:length(monthhourdata)
%                 fprintf(fn2,numformat,monthhourdata(p,:));
%                 fprintf(fn2,'\r\n');
%             end
%             fclose(fn2);
%             f=ftp('pc70.gvc.gu.se','urban-net');
%             cd(f,'public_html');
%             cd(f,'GVCdata');
%             mput(f,['C:\MeteorologicalMeasurements\GVCroof\Data\MonthlyFiles2011_Now\gvc_roof_60mindata_' num2str(year1) '_' num2str(lmonth) '.txt']);
            
            
        end
    end
    
    GVC_plot_english_v3(n,tendata)
    GVC_plot_swedish_v2(n,tendata)
    
    filename = 'C:\MeteorologicalMeasurements\GVCroof\Data\GVCdata_Last4Days.csv';
    GVC_export_recent_v1(n,tendata,filename);
    f=ftp('pc70.gvc.gu.se','urban-net');
    cd(f,'public_html');
    mput(f,filename);
  exit;
    
catch err
   msg=getReport(err);
   setpref('Internet','SMTP_Server','smtp.gu.se')
   
%    setpref('Internet','E_mail','per.weslien@gu.se')
%    sendmail('per.weslien@gu.se','Error in roof_plot_v3.m',msg)
%    
%    setpref('Internet','E_mail','frans.olofson@gu.se')
%    sendmail('frans.olofson@gu.se','Error in roof_plot_v4.m',msg)
   setpref('Internet','E_mail','fredrikl@gvc.gu.se')
   sendmail('fredrikl@gvc.gu.se','Error in roof_plot_v3.m',msg)
   disp('error')
   exit;
end


%%

%     %% Plot initialisation - MOVED to SUBFUNCTIONS
%     startday=n-3;
%     X1=startday:10/1440:n+1;
%     plotdata=NaN(length(X1),size(tendata,2));
%     plotdata(:,1)=X1';
%     index=1;
%     for i=1:size(plotdata,1)
%         line2=find(plotdata(i,1)==tendata(:,1));
%         if line2>1
%             if size(tendata,1)>index
%                 plotdata(i,:)=tendata(line2,:);
%                 index=index+1;
%             end
%         end
%     end
%
% %     startday=n-3;
% %     X1=startday:10/1440:n+1;
% %     plotdata=NaN(length(X1),size(tendata,2));
% %     plotdata(:,1)=X1';
% %     index=1;
% %     for i=1:size(plotdata,1)
% %         line2=find(plotdata(index,1)==tendata(:,1));
% %         if line2>1
% %             if size(tendata,1)>index
% %                 plotdata(index,:)=tendata(line2,:);
% %                 index=index+1;
% %             end
% %         end
% %     end
%
%
%
%
%
%
% %     figure1 = figure('Paperunits','inches','Paperposition',[0 -5 3.06 5.0],'color',[1 1 1]);
%
%     figure1 = figure('Position',[50 50 460 700],'color',[1 1 1]);
%
%     xlabels={'0',' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'...
%     ,' ',' ','6',' ',' ','12',' ',' ','18',' ',' ','0'};
%     xlabels2={' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '...
%     ,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
%
%     tsize=10;
%     ysize=10;
%     asize=9;
%     %% Temperature and humidity
%     axes1 = axes('Parent',figure1,...
%     'YLim',[0 1000],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.11 0.84 0.80 0.13],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels2,...
%     'XTick',n-43:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Air temperature and relative humidity','FontSize', tsize);
%     [plot6 left6 right6]=plotyy(plotdata(:,1),plotdata(:,5),plotdata(:,1),plotdata(:,6));
%     set(plot6(2),'FontSize',asize)
%     set(left6(1),'DisplayName','T_{AIR}','Color',[0 0 1]);
%     set(right6(1),'DisplayName','RH','Color',[0 1 0]);
%
%     % Create ylabel
%     set(plot6(1),'YLim',[-10 40])%(ymax+2)
%     set(plot6(1),'Ytick',[-10 0 10 20 30 40])
%     set(plot6(2),'YLim',[0 100])
%     set(plot6(2),'Ytick',[0 20 40 60 80 100])
%     set(plot6(1),'XTickLabel',xlabels2)
%     set(plot6(2),'XTickLabel',xlabels2)
%     set(plot6(1),'XTick',n-3:1/12:n+1);
%     set(plot6(2),'XTick',n-3:1/12:n+1);
%     set(plot6(2),'TickLength',[0.005 0.15]);
%     set(get(plot6(1),'Ylabel'),'String','T ( ^oC )','FontSize',ysize,'Color',[0 0 0])
%     set(get(plot6(2),'Ylabel'),'String','RH (%)','FontSize',ysize,'Color',[0 0 0])
% %     legend1 = legend(axes1,'show');
% %     set(legend1,'Position',[0.72 0.77 0.05 0.01],'Orientation','horizontal','FontSize',6,...
% %     'FontName','Arial');
%
%     %% Radiation
%     axes2 = axes('Parent',figure1,...
%     'YLim',[0 1000],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.12 0.66 0.80 0.13],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels2,...
%     'XTick',n-3:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Incoming radiation','FontSize', tsize);
%     plot1=plot(plotdata(:,1),plotdata(:,[15 16 19]));
%     set(plot1(1),'DisplayName','K_{Total}','Color',[0 0 0],'LineStyle','-');
%     set(plot1(2),'DisplayName','K_{Diffuse}','Color',[1 0 0],'LineStyle','-');
%     set(plot1(3),'DisplayName','L ','Color',[0 0 1],'LineStyle','-');
%     legend1 = legend(axes2,'show');
%     set(legend1,'Position',[0.48 0.632 0.1 0.01],'Orientation','horizontal','FontSize',8,...
%     'FontName','Arial');
%     ylabel('Radiation (W m^{-2})','FontSize',ysize);
%
%     %% Pressure
%     axes3 = axes('Parent',figure1,...
%     'YLim',[980 1080],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.12 0.445 0.80 0.13],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels2,...
%     'XTick',n-3:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Pressure','FontSize', tsize);
%     plot2=plot(plotdata(:,1),plotdata(:,12));
%
%     ylabel('Pressure (hPa)','FontSize',ysize);
%
%     %% Windspeed
%     axes4 = axes('Parent',figure1,...
%     'YLim',[0 20],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.12 0.32 0.80 0.075],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels2,...
%     'XTick',n-3:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Wind speed','FontSize', tsize);
%     plot3=plot(plotdata(:,1),plotdata(:,7));
%
%     ylabel('WSpd (m s^{-1})','FontSize',ysize);
%
%     %% Winddirection
%     axes5 = axes('Parent',figure1,...
%     'YLim',[0 360],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.12 0.20 0.80 0.075],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels2,...
%     'YTickLabel',[0 90 180 270 360],...
%     'YTick',0:90:360,...
%     'XTick',n-3:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Wind direction','FontSize', tsize);
%     plot4=plot(plotdata(:,1),plotdata(:,8));
%     set(plot4,'Color',[0 0 1],'LineStyle','.','Markersize',5);
%
%     ylabel('WDir ( ^o )','FontSize',ysize);
%
%     %% Precipitation
%     axes6 = axes('Parent',figure1,...
%     'YLim',[0.001 3],...
%     'XLim',[n-3 n+1],...
%     'Position',[0.12 0.07 0.80 0.075],...
%     'FontSize',asize,...
%     'XTickLabel',xlabels,...
%     'XTick',n-3:1/12:n+1,...
%     'TickLength',[0.005 0.1]);
%     box('on');
%     hold('all');
%     title('Precipitation','FontSize', tsize);
% %     prec=plotdata(:,10);
% %     prec(isnan(prec))=0;
%     plot5=bar(plotdata(:,1),plotdata(:,10),'k');
%     set(plot5(1),'DisplayName','Precipitation');
%     ylabel('mm/10min','FontSize',ysize);
% %     vec_pos = get(get(gca, 'XLabel'), 'Position');
% %     set(get(gca, 'XLabel'), 'Position', vec_pos + [0 0.5 0]);
%     xlabel('Time (h)','FontSize',ysize);
%
%     %% Dates labes
%     text(n-3+3.2,-2.5,datestr(n,29),'FontSize',10)
%     text(n-3+2.2,-2.5,datestr(n-1,29),'FontSize',10)
%     text(n-3+1.2,-2.5,datestr(n-2,29),'FontSize',10)
%     text(n-3+0.2,-2.5,datestr(n-3,29),'FontSize',10)
%     %% Save graphs for web
%     % i1=num2str(2011);i2=num2str(08,'%2.2d');i3=num2str(01,'%2.2d');i4=num2str(23,'%2.2d');
%     % savtitle=['GVC_roof_',i1,i2,i3,'T',i4,'5734.png'];
%     savtitle=['GVC_roof_',datestr(round(now),30),'.png'];
%     PlotDir=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot\Figures');
%     figurea=fullfile(PlotDir,savtitle);
% %     saveas(figure (1), figurea)
%     set(figure1,'PaperPositionMode','auto')
%     print(figure1,'-dpng',figurea)
% %     d=getframe(figure1);
% %     imwrite(d.cdata, figurea)
% %     pause(10)
%     webtitle='GVC_plot.png';
%     PlotDir1=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot');
%     figurea1=fullfile(PlotDir1,webtitle);
% %     saveas(figure (1), figurea1);
% %     set(figure1,'PaperPositionMode','auto')
%     print(figure1,'-dpng',figurea1)
% %     d=getframe(figure1);
% %     imwrite(d.cdata, figurea1)
% %     pause(10)
%     f=ftp('pc70.gvc.gu.se','urban-net');
%     cd(f,'public_html');
%     mput(f,'GVC_plot.png');
%
%
%     % Tablefigure
%     last=size(tendata,1);
%     fsize=5;
%     figure2 = figure('Position',[500 200 294 120],'color',[1 1 1]);
%         annotation(figure2,'textbox',[0.00 0.9 0.85 0.1],...
%     'String',['Last downloaded data at:     ' datestr(tendata(last,1),'mmmm dd, yyyy HH:MM')],...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
%     annotation(figure2,'textbox',[0.00 0.75 0.85 0.1],...
%     'String',{'Air Temperature: '
%               'Relative humidity:'
%               'Wind speed:      '
%               'Wind direction:  '
%               'Pressure (75 masl): '
%               'Precepitation (rain):    '
%               'Global radiation:'
%               'Diffuse radiation:'
%               'Incoming longwave radiation:'},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize);
%     annotation(figure2,'textbox',[0.55 0.75 0.85 0.1],...
%     'String',{num2str(tendata(last,5),'%6.1f')
%               num2str(tendata(last,6),'%6.1f')
%               num2str(tendata(last,7),'%6.1f')
%               num2str(tendata(last,8),'%6.1f')
%               num2str(tendata(last,12),'%6.1f')
%               num2str(tendata(last,10),'%6.0f')
%               num2str(tendata(last,15),'%6.1f')
%               num2str(tendata(last,16),'%6.1f')
%               num2str(tendata(last,19),'%6.1f')},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize,'FontWeight','bold');
%     annotation(figure2,'textbox',[0.73 0.75 0.85 0.1],...
%     'String',{' °C'
%               ' %'
%               ' m/s'
%               ' °'
%               ' hPa'
%               ' mm/10 min'
%               ' W m-2'
%               ' W m-2'
%               ' W m-2'},...
%     'LineStyle','none','FontName','Verdana','FontSize',fsize);
%
%     webtitle='GVCtable_plot.png';
%     PlotDir1=fullfile('C:\MeteorologicalMeasurements\GVCroof\Plot');
%     figurea2=fullfile(PlotDir1,webtitle);
%
%     set(figure2,'PaperPositionMode','auto')
% %     saveas(figure (2), figurea2)
%     print(figure2,'-dpng',figurea2)
%
%     f=ftp('pc70.gvc.gu.se','urban-net');
%     cd(f,'public_html');
%     mput(f,'GVCtable_plot.png');

%     setpref('Internet','SMTP_Server','smtp.gu.se')
%     setpref('Internet','E_mail','fredrikl@gvc.gu.se')
%     sendmail('fredrikl@gvc.gu.se','roof_plot_v3.m','runned with succes')